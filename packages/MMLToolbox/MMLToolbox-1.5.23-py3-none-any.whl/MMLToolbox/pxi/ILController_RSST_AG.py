import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.integrate
import PXIPostProcessing
from scipy.fft import fft, ifft, fftfreq


from MMLToolbox.pxi.StoreSetup import StoreSetup
from MMLToolbox.pxi.SignalHandler import SignalHandler
from MMLToolbox.pxi.PXIHandler import PXIHandler
from MMLToolbox.util.types import *

MU_0 = 4*np.pi*1e-7


class ILController_RSST_AG:
    def __init__(self, storeSetup:StoreSetup, meas_type=str, cutfrequency:int=1000, I_limit=30, U_limit=450,maxIterations=5,n_mean=1):
        self.ss = storeSetup
        self.meas_type = meas_type
        self.signal_handler = SignalHandler(storeSetup,meas_type)
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
        self.phase_shift = None
        self.B_shift = None

        # ILC Parameter
        self.cutfrequency = cutfrequency
        self.frequency = self.ss.readInfoValue("frequency")
        self.sample_freq = self.ss.readInfoValue("sampleFrequency")
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
        self.rohrer_voltage_factor = self.ss.readInfoValue("Rohrer_voltage_factor")

        # Killme Parameter, just for testing
        self.B_iter = []
        self.U_output_iter = []
        self.err_iter = []
        self.U_B_iter = []

    def doInitMeasurement(self):
        signal = self.signal_handler.getBaseOutSignal()*self.U_init
        self.pxi_handler.doMeasurement(signal=signal,iteration=self.steps_iteration)
        self.__postprocessing_measurement_data()
        self.__check_correlation_init_and_meas()
        self.phase_shift = self.__get_phase_shift(ref_signal=signal,shift_signal=self.B_meas)
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

            for ilc_iter in range(self.max_iterations):
                self.ilc_iter = ilc_iter
                self.__shift_signal()
                self.__compute_error()
                self.__check_stopping_criteria()
                signal = self.__get_new_excitation_signal()
                self.__check_voltage_and_current_limit_reached()
                self.pxi_handler.doMeasurement(signal=signal,iteration=steps_iter)
                self.__postprocessing_measurement_data()
                self.U_output_iter.append(self.U_output[1,:])
                self.U_output = signal[:,self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
                self.B_iter.append(self.B_meas[1,:])
                self.err_iter.append(self.err[1,:])
                self.U_B_iter.append(self.U_B_meas[1,:])
            self.__store_ilc_iteration_values()    
        np.savetxt("B_iter.txt",self.B_iter)
        np.savetxt("U_output_iter.txt",self.U_output_iter)
        np.savetxt("err_iter.txt",self.err_iter)
        np.savetxt("U_B_iter.txt",self.U_B_iter)

    def __compute_error(self):
        if self.frequency > self.cutfrequency:
            err = self.U_B_ref-self.U_B_meas
            self.tol = np.max(self.U_B_ref)*0.03
            self.FF_tol = 1.111+0.0111
        else:
            err = self.B_ref-self.B_shift
            self.tol = np.max(self.B_ref)*0.03
            self.FF_tol = 1.111+0.0111 # Bei Franz nix definiert, nehme an dass das passt
        
        err[:self.signal_handler.len_zeros] = 0
        err[:-self.signal_handler.len_zeros] = 0
        self.err = err


    def __check_stopping_criteria(self):
        S = np.sqrt(np.mean(self.err**2,axis=1))
        U_B_eff = np.sqrt(np.mean(self.U_B_meas**2, axis=1))  # RMS for each row
        U_B_glr = np.mean(np.abs(self.U_B_meas), axis=1)      # Mean absolute value for each row

        B_eff = np.sqrt(np.mean(self.B_shift**2, axis=1))      # RMS for each row
        B_glr = np.mean(np.abs(self.B_shift), axis=1) 

        if self.frequency > self.cutfrequency:
            FF = U_B_eff/U_B_glr
        else:
            FF = B_eff/B_glr 

        self.S.append(S)
        self.FF.append(FF)

        if np.all(S < self.tol) and np.all(FF<self.FF_tol):
            sys.exit(f"Criteria are for {self.B_values[self.steps_iteration]} fullfilled!")

    def __get_new_excitation_signal(self):
        U_new = self.U_output + self.k_p*self.err
        U_max = np.max(U_new,axis=1).reshape(2,-1)
        U_up = self.signal_handler.up_signal*U_max
        U_down = self.signal_handler.down_signal*U_max
        self.U_output = np.concatenate((U_up,U_new,U_down),axis=1)/self.rohrer_voltage_factor
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

        return k_p.reshape(2,-1)
        
    def __postprocessing_measurement_data(self):
        U_B_meas_x = self.__read_data_from_store_setup("Bx")
        U_B_meas_y = self.__read_data_from_store_setup("By")
        self.U_B_meas = np.array([U_B_meas_x,U_B_meas_y])

        B_meas_x = self.__U_B_to_B("Bx",U_B_meas_x)
        B_meas_y = self.__U_B_to_B("By",U_B_meas_y)
        self.B_meas = np.array([B_meas_x,B_meas_y])

        U_meas_x = self.__read_data_from_store_setup("Ux")*self.ss.readInfoValue("Rohrer_voltage_factor")
        U_meas_y = self.__read_data_from_store_setup("Uy")*self.ss.readInfoValue("Rohrer_voltage_factor")
        self.U_meas = np.array([U_meas_x,U_meas_y])

        I_meas_x = self.__read_data_from_store_setup("Ix")*self.ss.readInfoValue("Rohrer_current_factor")
        I_meas_y = self.__read_data_from_store_setup("Iy")*self.ss.readInfoValue("Rohrer_current_factor")
        self.I_meas = np.array([I_meas_x,I_meas_y])

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
        int_data = int_data - (max(int_data)+min(int_data))/2
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

    def __get_phase_shift(self,ref_signals,shift_signals):
        phase_shift = []
        for ref_signal, shift_signal in zip(ref_signals,shift_signals):
          signal_A = ref_signal[self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
          signal_B = shift_signal[self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
          temp_A = PXIPostProcessing.calc_average(signal_A,self.sample_freq,self.frequency,1)
          temp_B = PXIPostProcessing.calc_average(signal_B,self.sample_freq,self.frequency,1)

          spectrum_A = fft(temp_A)
          spectrum_B = fft(temp_B)
          n = len(temp_B)

          positive_magnitudes = np.abs(spectrum_A[:n // 2])
          dominant_idx = np.argmax(positive_magnitudes[1:]) + 1  

          phase_A = np.angle(spectrum_A[dominant_idx])
          phase_B = np.angle(spectrum_B[dominant_idx])
          phase_difference = phase_B - phase_A

          temp_phase_shift = int(np.round((phase_difference / (2 * np.pi)) * n))
          phase_shift.append(temp_phase_shift)
        return np.array(phase_shift).reshape(2,-1)
    
    def __shift_signal(self):
        shift_signals = []
        for signal,shift in zip(self.B_meas,self.phase_shift):
            temp = np.roll(signal,shift)
            shift_signals.append(temp)
        self.B_shift = np.array(shift_signals).reshape(2,-1)

    def __phase_shift_meas_and_ref(self):
        #TODO: Kann sein, dass wir für die Messungen noch einen Filter brauchen, wenn das Messsignal zu Noise wird.
        temp_B_ref = self.signal_handler.getBaseRefSignal()
        ref_signal = []

        for row_ref,row_meas in zip(temp_B_ref,self.B_meas):
            if np.all(row_ref == 0):
                zero_crossing_B_meas = 0
                zero_crossing_B_ref = 0
            else:
                zero_crossing_B_meas = np.where(np.diff(np.sign(row_meas)))[0][0]
                zero_crossing_B_ref = np.where(np.diff(np.sign(row_ref)))[0][0]

            phase =  zero_crossing_B_meas - zero_crossing_B_ref
            ref_signal.append(np.roll(row_ref,phase))

        self.ref_signal = np.array(ref_signal).reshape(2,-1)

    def __define_ref_signal(self,B_amp):
        self.B_ref = self.signal_handler.getBaseOutSignal()*B_amp
        U_B_x = self.__B_to_U_B("Bx",self.B_ref[0,:])
        U_B_y = self.__B_to_U_B("By",self.B_ref[1,:])
        self.U_B_ref = np.array([U_B_x, U_B_y])

    def __check_voltage_and_current_limit_reached(self):
        if np.max(self.U_output) > self.U_limit or np.max(self.I_meas) > self.I_limit:
            sys.exit(f"U > {self.U_limit:.2f} or I > {self.I_limit:.2f}")

    def __store_ilc_iteration_values(self):
        self.ss.writeData(self.steps_iteration,"FF",self.FF)
        self.ss.writeData(self.steps_iteration,"S",self.S)
