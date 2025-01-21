import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.integrate

from . import StoreSetup
from . import PXIPostProcessing
from . import SignalFormHandler
from . import PXIHandler
from MMLToolbox.util.types import *

MU_0 = 4*np.pi*1e-7


class ILController_RSST_AG:
    def __init__(self, storeSetup:StoreSetup, meas_type=str, cutfrequency:int=30, I_limit=30, U_limit=450,maxIterations=10,n_mean=1):
        self.ss = storeSetup
        self.meas_type = meas_type
        self.signal_handler = SignalFormHandler(storeSetup,meas_type)
        self.pxi_handler = PXIHandler(storeSetup)

        # Measurement Parameter
        self.U_init = storeSetup.readInfoValue("U_init")
        self.B_values = storeSetup.readInfoValue("B_values")
        self.steps_iteration = 0
        self.U_B_meas = None
        self.B_meas = None
        self.U_meas = None
        self.I_meas = None

        # Signal
        self.B_ref = None
        self.U_B_ref = None
        self.ref_signal = None
        self.U_output = None

        # ILC Parameter
        self.cutfrequency = cutfrequency
        self.frequency = self.ss.readInfoValue("frequency")
        self.k_p = None
        self.max_iterations = maxIterations
        self.err = None
        self.ilc_iter = None
        self.FF_tol = 0
        self.tol = 0
        self.FF = None
        self.S = None
        self.I_limit = I_limit
        self.U_limit = U_limit
        # self.maxIterations = maxIterations
        # self.S = []
        # self.FF = []
        # self.amp_e_up = np.linspace(0,1,len(self.upSteps))
        # self.amp_e_down = np.linspace(1,0,len(self.downSteps))
        # self.Imax = Imax
        # self.Umax = Umax        
        # self.U_ref = None
        # self.B_ref = None
        # self.first_iteration = None
        # self.U_out = None
        # self.n_mean = n_mean
        # self.k_p = None
        # self.err = None

        # Additional Parameter
        # self.J_corr = None
        # self.I1_temp = None
        # self.M_corr = None
        # self.B_corr = None
        # self.B_corr_temp = None
        # self.U_temp = None

    def doInitMeasurement(self):
        signal = self.signal_handler.getBaseOutSignal()*self.U_init
        self.pxi_handler.doMeasurement(signal=signal,iteration=self.steps_iteration)
        self.__postprocessing_measurement_data()
        self.__check_correlation_init_and_meas()
        self.__phase_shift_meas_and_ref()
        self.k_p = self.__getILCFactor()
        self.U_output = signal
        
    def startILCAlgorithm(self):
        #TODO: Was verwenden wir als Init Signal und auch für die weiteren Iterationen?
        for steps_iter,B_value in enumerate(self.B_values):
          self.steps_iteration = steps_iter
          Bx_iter = []
          By_iter = []
          Ux_iter = []
          Uy_iter = []
          self.FF = []
          self.S = []

          self.doInitMeasurement()
          self.__define_ref_signal(B_value)

          for ilc_iter in self.max_iterations:
              self.ilc_iter = ilc_iter
              self.__compute_error()
              self.__check_stopping_criteria()
              signal = self.__get_new_excitation_signal()
              self.__check_voltage_and_current_limit_reached()
              self.pxi_handler.doMeasurement(signal=signal,iteration=steps_iter)
          self.__store_ilc_iteration_values()    


    def __compute_error(self):
        if self.frequency > self.cutfrequency:
            self.err = self.U_B_ref-self.U_B_meas
            self.tol = np.max(self.U_B_ref)*0.03
            self.FF_tol = 1.111+0.0111
        else:
            self.err = self.B_ref-self.B_meas
            self.tol = np.max(self.B_ref)*0.03
            self.FF_tol = 1.111+0.0111 # Bei Franz nix definiert, nehme an dass das passt
          
    def __check_stopping_criteria(self):
        S = np.sqrt(np.mean(self.err**2,axis=1))
        U_B_eff = np.sqrt(np.mean(self.U_B_meas**2, axis=1))  # RMS for each row
        U_B_glr = np.mean(np.abs(self.U_B_meas), axis=1)      # Mean absolute value for each row

        B_eff = np.sqrt(np.mean(self.B_meas**2, axis=1))      # RMS for each row
        B_glr = np.mean(np.abs(self.B_meas), axis=1) 

        if self.frequency > self.cutfrequency:
            FF = U_B_eff/U_B_glr
        else:
            FF = B_eff/B_glr 

        self.S.append(S)
        self.FF.append(FF)

        if S < self.tol and FF<self.FF_tol:
            sys.exit(f"Criteria are for {self.B_values[self.steps_iteration]} fullfilled!")

    def __get_new_excitation_signal(self):
        U_output = self.U_output[self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
        U_new = U_output + self.k_p*self.err
        U_max = np.max(U_new,axis=1).reshape(2,-1)
        U_up = self.signal_handler.up_signal*U_max
        U_down = self.signal_handler.down_signal*U_max
        self.U_output = np.concatenate((U_up,U_new,U_down),axis=1)
        return self.U_output

    def __getILCFactor(self):
        U_meas_peak = np.max(self.U_meas,axis=1)
        U_B_peak = np.max(self.U_B_meas,axis=1)
        B_peak = np.max(self.B_meas,axis=1)

        k_sys_U = U_B_peak/U_meas_peak
        k_sys_B = B_peak/U_meas_peak

        if self.frequency > self.cutfrequency:
            k_p = 1/k_sys_U
        else:
            k_p = 1/k_sys_B 

        return k_p
        
    def __postprocessing_measurement_data(self):
        U_B_meas_x = self.__read_data_from_store_setup("Bx")
        U_B_meas_y = self.__read_data_from_store_setup("By")
        self.U_B_meas = np.array([[U_B_meas_x],[U_B_meas_y]])

        B_meas_x = self.__U_B_to_B("Bx",U_B_meas_x)
        B_meas_y = self.__U_B_to_B("By",U_B_meas_y)
        self.B_meas = np.array([[B_meas_x],[B_meas_y]])

        U_meas_x = self.__read_data_from_store_setup("Ux")*self.ss.readInfoValue("Rohrer_voltage_factor")
        U_meas_y = self.__read_data_from_store_setup("Uy")*self.ss.readInfoValue("Rohrer_voltage_factor")
        self.U_meas = np.array([[U_meas_x],[U_meas_y]])

        I_meas_x = self.__read_data_from_store_setup("Ix")*self.ss.readInfoValue("Rohrer_current_factor")
        I_meas_y = self.__read_data_from_store_setup("Iy")*self.ss.readInfoValue("Rohrer_current_factor")
        self.I_meas = np.array([[I_meas_x],[I_meas_y]])

    def __read_data_from_store_setup(self,name):
        len_up = self.signal_handler.len_up_signal
        len_down = self.signal_handler.len_down_signal
        return self.ss.readData(self.steps_iteration,name)[len_up:-len_down]
    
    def __U_B_to_B(self,name,data):
        area = self.ss.readInfoValue(f"{name}_mat_area")
        amp = self.ss.readInfoValue(f"B_amp")
        turns = self.ss.readInfoValue(f"B_turns")
        t = self.ss.readInfoValue("time")
        
        mean_data = data - np.mean(data)
        int_data = scipy.integrate.cumtrapz(mean_data,t,initial=0)/(amp*turns*area)
        return int_data
    
    def __B_to_U_B(self,name,data):
        sample_frequency = self.ss.readInfoValue("sampleFrequency") 
        area = self.ss.readInfoValue(f"{name}_mat_area")
        amp = self.ss.readInfoValue(f"B_amp")
        turns = self.ss.readInfoValue(f"B_turns")
        dB_grad = np.gradient(data)
        U_B = (turns*area*amp*sample_frequency)*dB_grad
        return U_B
    
    def __check_correlation_init_and_meas(self):
        if (max_B_meas:=np.max(np.abs(self.B_meas))) > self.B_values[0]*1.3:
              sys.exit(f"Please decrease U_init!\n max_B_meas={max_B_meas:.2f}\n B_wanted={self.B_values[0]:.2f}")
        elif (max_B_meas:=np.max(np.abs(self.B_meas))) < self.B_values[0]*0.7:
              sys.exit(f"Please increase U_init! \n max_B_meas={max_B_meas:.2f}\n B_wanted={self.B_values[0]:.2f}") 

    def __phase_shift_meas_and_ref(self):
        temp_B_ref = self.signal_handler.getBaseRefSignal()
        zero_crossing_B_ref = np.array([np.where(np.diff(np.sign(row)))[0] for row in temp_B_ref])
        zero_crossing_B_meas = np.array([np.where(np.diff(np.sign(row)))[0] for row in self.B_meas])
        phase_correction = (zero_crossing_B_meas - zero_crossing_B_ref).reshape(2,-1)
        self.ref_signal = np.array(np.roll(data,phase) for data,phase in zip(temp_B_ref,phase_correction)).reshape(2,-1)

    def __define_ref_signal(self,B_amp):
        self.B_ref = self.ref_signal*B_amp
        self.U_B_ref = np.array([[self.__B_to_U_B("Bx",self.B_ref[0,:])],[self.__B_to_U_B("By",self.B_ref[1,:])]])

    def __check_voltage_and_current_limit_reached(self):
        if np.max(self.U_output) > self.U_limit or np.max(self.I_meas) > self.I_limit:
            sys.exit(f"U > {self.U_limit:.2f} or I > {self.I_limit:.2f}")

    def __store_ilc_iteration_values(self):
        self.ss.writeData(self.steps_iteration,"FF",self.FF)
        self.ss.writeData(self.steps_iteration,"S",self.S)
