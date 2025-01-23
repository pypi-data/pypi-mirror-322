import numpy as np
import yaml
import math
from CoolProp.CoolProp import PropsSI

from pollux_model.heat_pump.NREL_components.utilities.libraries import refrigerants
from pollux_model.heat_pump.NREL_components.utilities.unit_defs import ureg, Q_


class HeatPumpModel:
    def __init__(self):
        # 1.COP
        # Outputs
        self.ideal_COP = np.array([-1.0] * 2) * ureg.dimensionless
        self.actual_COP = np.array([-1.0] * 2) * ureg.dimensionless
        self.refrigerant = []

        # 2.Energy and Mass Flow
        # Outputs
        self.cold_final_temperature = Q_(np.array([-1.0] * 2), 'degC')
        self.power_in = Q_(np.array([-1.0] * 2), 'W')  # Gives the

    def construct_yaml_input_quantities(self, file_path):
        with open(file_path, "r") as file_desc:
            input_dict = yaml.safe_load(file_desc)

        for key in input_dict:
            var = input_dict[key]
            try:
                if not isinstance(var, dict):
                    continue
                else:
                    quant = Q_(var['val'], var['unit'])
                input_dict[key] = quant
            except KeyError:
                print('Something is wrong with input variable ' + key)
                quit()
        self.__dict__.update(input_dict)

    # Model Calculations
    # Calculating COP
    def calculate_COP(self):
        # Calculating the ideal COP to begin with, this will be independent of the future anlaysis.
        self.ideal_COP = (((self.hot_temperature_desired.to('degK') + self.hot_buffer.to('degK'))) /
                          (
                                  (self.hot_temperature_desired.to('degK') +
                                   self.hot_buffer.to('degK')) - (
                                          self.cold_temperature_available.to('degK') -
                                          self.cold_buffer.to('degK'))))

        if self.second_law_efficiency_flag is True:
            # If the carnot efficiency factor is true calculation the actual COP
            self.actual_COP = self.ideal_COP * self.second_law_efficiency
        else:
            # If the carnot efficiency factor is false requires more work in several steps
            # 1. If no refrigerant is selected pick one
            # 2. Using selected refrigerant calculate compressor efficiency
            # 3. Calculate actual COP from
            # compressor efficiency
            # 4. Throw an error if calculation could not be completed.

            # Below will attempt to choose a
            # refrigerant and calculate a realistic compressor efficiency from it,
            # if this fails, it will revert to the carnot efficiency factor methodology
            # Estimating Refrigerant Performance
            if self.refrigerant_flag is not True:
                self.refrigerant = []
                for test_refrigerant in refrigerants:
                    t_crit = Q_(PropsSI(test_refrigerant, 'Tcrit'), 'kelvin').to('degC')
                    # Checking if the refrigerant's critical temperature
                    # is at least 30°C > than the process temp.
                    if t_crit > (np.amax(self.hot_temperature_desired) + self.t_crit_delta):
                        self.refrigerant.append(test_refrigerant)

                print('Potential refrigerants include: ', self.refrigerant)
                # Here the refrigerant with the lowest critical pressure,
                # and therefore hopefully the lowest compression ratio
                # is found and that will be recommended
                # Need to update to reflect the fact that best refrigerant
                # might not be the one with the lowest critical pressure
                min_p_crit = Q_('1e9 Pa')
                for test_refrigerant in self.refrigerant:
                    p_crit = Q_(PropsSI(test_refrigerant, 'Pcrit'), 'Pa')
                    if p_crit < min_p_crit:
                        min_p_crit = p_crit
                        self.refrigerant = test_refrigerant

            if self.print_results:
                print('Selected refrigerant (based on user selection or minimual p_crit) is: ',
                      self.refrigerant)

            # Adjust such that this is below the Carnot Efficiency Factor
            # Cycle calculation
            # Here the cycle points will be calculated. These points are:
            #  1. Compressor inlet
            #  2. Compressor outlet
            #  3. Expansion valve inlet
            #  4. Expansion valve outlet
            #  2-3 is the condenser where heat is expelled
            #  from the heat pump condenser to the heat sink or high
            #  temperature working fluid stream
            #  4-1 is the evaporator where heat is absorbed
            #  from the heat source or cold temperature working fluid to the heat pump evaporator
            self.refrigerant_high_temperature = (self.hot_temperature_desired.to(ureg.degK)
                                                 + self.hot_buffer.to(
                        ureg.degK))
            self.refrigerant_low_temperature = (self.cold_temperature_available.to(ureg.degK)
                                                - self.cold_buffer.to(
                        ureg.degK))

            try:
                T_1 = np.array(self.refrigerant_low_temperature.m)
                T_3 = np.array(self.refrigerant_high_temperature.m)

                # Calculating Cycle Parameters
                P_1 = PropsSI('P', 'T', T_1, 'Q', 1, self.refrigerant)
                S_1 = PropsSI('S', 'T', T_1, 'Q', 1, self.refrigerant)
                H_1 = PropsSI('H', 'T', T_1, 'Q', 1, self.refrigerant)

                P_3 = PropsSI('P', 'T', T_3, 'Q', 0, self.refrigerant)
                # S_3 = PropsSI('S', 'T', T_3, 'Q', 0, self.refrigerant)
                S_3 = PropsSI('S', 'T', T_3, 'Q', 0, self.refrigerant)
                H_3 = PropsSI('H', 'T', T_3, 'Q', 0, self.refrigerant)
                P_4 = P_1
                H_4 = H_3
                T_4 = PropsSI('T', 'P', np.round(P_4, 2), 'H',
                              np.round(H_4, 2), self.refrigerant)
                S_4 = PropsSI('S', 'H', np.round(H_4, 2), 'P',
                              np.round(P_4, 2), self.refrigerant)

                if len(T_1) == 1:
                    T_2 = PropsSI('T', 'S', np.round(S_1, 2), 'P',
                                  np.round(P_3, 2), self.refrigerant)
                    # T_2 = PropsSI('T', 'S',
                    #               np.round(S_1, 2), 'P', np.round(P_3, 2), self.refrigerant)
                    H_2 = PropsSI('H', 'S',
                                  np.round(S_1, 2), 'P',
                                  np.round(P_3, 2), self.refrigerant)

                    P_2 = P_3
                    S_2 = PropsSI('S', 'H', np.round(H_2, 2), 'P',
                                  np.round(P_2, 2), self.refrigerant)

                    H_2_prime = PropsSI('H', 'S',
                                        np.round(S_1, 2),
                                        'P', np.round(P_3, 2), self.refrigerant)
                    H_2 = H_1 + (H_2_prime - H_1) / (
                        self.compressor_efficiency.m)  # Remark,
                    # it should be tested if the state 2 (H_2, P_2) is in the 2-phase region or not
                    # T_2 = PropsSI('T', 'H',
                    #               np.round(H_2, 2), 'P',
                    #               np.round(P_2, 2), self.refrigerant)
                    self.actual_COP = (np.divide((H_2 - H_3), (H_2 - H_1))) * ureg.dimensionless

                    # TODO:CODE FOR POWER INPUT,NEED TO CHECK
                    if self.electricity_power_in.m != 'NaN':
                        self.m_refrigerant = self.electricity_power_in.m / ((H_2 - H_1))
                        print('Refrigerant mass flow rate(kg/s):', self.m_refrigerant)
                        self.pr_heat_rej = Q_(self.m_refrigerant * ((H_2 - H_3)), 'W')
                        print('calc_heat rejection:', self.pr_heat_rej)
                        print('Power_input:', self.electricity_power_in.m)
                        H_2input = self.electricity_power_in.m / 2 + H_1
                        print('H_2:', H_2)
                        print('H_2_input:', H_2input)
                        self.actual_COP_input = (np.divide((H_2input - H_3),
                                                           (H_2 - H_1))) * ureg.dimensionless
                        print('COP_INPUT:', self.actual_COP_input)
                    else:
                        self.m_refrigerant = 'NaN'
                    # self.m_refrigerant = self.electricity_power_in.m / ((H_2 - H_1))
                    # # print('Refrigerant mass flow rate(kg/s):', self.m_refrigerant)
                    # self.pr_heat_rej = self.m_refrigerant*((H_2 - H_3))
                    # # print('calc_heat rejection:',  self.pr_heat_rej)
                    # # print('H_2:', H_2)
                    # # print('Power_input:', self.power_demand.m)
                    # H_2input = self.electricity_power_in.m / 2 + H_1
                    # # print('H_2_input:', H_2input)
                    # self.actual_COP_input = \
                    #     (np.divide((H_2input - H_3), (H_2 - H_1))) * ureg.dimensionless
                    # # print('COP_INPUT:', self.actual_COP_input)
                else:
                    # T_2 = PropsSI('T', 'S', S_1, 'P', P_3, self.refrigerant)
                    H_2 = PropsSI('H', 'S', S_1, 'P', P_3, self.refrigerant)

                    P_2 = P_3
                    H_2_prime = PropsSI('H', 'S', S_1, 'P', P_3, self.refrigerant)
                    H_2 = H_1 + (H_2_prime - H_1) / (
                        self.compressor_efficiency.m)  # Remark,
                    # it should be tested if the state 2 (H_2, P_2) is in the 2-phase region or not
                    # T_2 = PropsSI('T', 'H',
                    #               np.round(H_2, 2),
                    #               'P', np.round(P_2, 2), self.refrigerant)
                    self.actual_COP = (np.divide((H_2 - H_3), (H_2 - H_1))) * ureg.dimensionless

                # There is an efficiency associated with the pressure
                # ratio and an efficiency association with the volume ratio
                # The VR is taken from experimental values which we
                # do not fully have, so will integrate as part of year 2
                # For now the VR is set to a constant value.
                # The compressor efficiency can also be set by the user
                PR = P_2 / P_1
                # eta_pr = 0.95-0.01*PR
                # eta_vr = 0.70
                # self.compressor_efficiency[i] = round(eta_vr*eta_pr, 3)
                # self.actual_COP = self.ideal_COP *
                # self.compressor_efficiency

            except TypeError:
                print('There was an error calling refrigerant properties.'
                      ' Please check inputs and try again.')
                quit()

        if self.print_results:
            print('Calculate COP Called')
        if self.print_results:
            print('Average Theoretical COP: ', np.mean(self.ideal_COP))
        if self.print_results:
            print('Average Estimated COP: ', np.mean(self.actual_COP))
        # if self.print_results: print('Compressor Power: ', np.mean(self.actual_COP))
        if self.print_results:
            print('Pressure ratio: ', PR)

        self.refrigerant_T = [float(self.refrigerant_low_temperature.m), float(T_2),
                              float(self.refrigerant_high_temperature.m), float(T_4), float(T_1)]
        self.refrigerant_H = [float(H_1), float(H_2), float(H_3), float(H_4), float(H_1)]
        self.refrigerant_S = [float(S_1), float(S_2), float(S_3), float(S_4), float(S_1)]

        self.refrigerant_P = [float(P_1), float(P_2), float(P_3), float(P_4), float(P_1)]

    # Calculating working fluid energy and mass balance
    def calculate_energy_and_mass_flow(self):
        if self.print_results:
            print('Calculate Energy and Mass Called')

        # Initializing Temporary Arrays
        # h_hi = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        # h_ho = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        # h_ci = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        #        h_co = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        h_hi_new = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        h_ho_new = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        h_ci_new = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')
        h_co_new = Q_(np.array([-1.0] * self.n_hrs), 'J/kg')

        # Calculating the Hot and Cold Mass Flow Parameters
        # h_hi = Q_(PropsSI('H', 'T', self.hot_temperature_minimum.to('degK').m,
        # 'P', self.hot_pressure.to('Pa').m,self.hot_refrigerant), 'J/kg')
        P_hi_q = PropsSI('P', 'T', self.hot_temperature_minimum.to('degK').m,
                         'Q', 0, self.hot_refrigerant)
        h_hi_new = Q_(PropsSI('H', 'T', self.hot_temperature_minimum.to('degK').m,
                              'Q', 0, self.hot_refrigerant), 'J/kg')
        S_hi_new = PropsSI('S', 'H', np.round(h_hi_new.to('J/kg').m, 2),
                           'P', np.round(P_hi_q, 2), self.hot_refrigerant)

        # h_ho = Q_(PropsSI('H', 'T', self.hot_temperature_desired.to('degK').m,
        #                   'P', self.hot_pressure.to('Pa').m,
        #                   self.hot_refrigerant), 'J/kg')
        P_ho_q = PropsSI('P', 'T', self.hot_temperature_desired.to('degK').m,
                         'Q', 0, self.hot_refrigerant)
        h_ho_new = Q_(PropsSI('H', 'T', self.hot_temperature_desired.to('degK').m,
                              'Q', 0, self.hot_refrigerant),
                      'J/kg')
        S_ho_new = PropsSI('S', 'H', np.round(h_ho_new.to('J/kg').m, 2),
                           'P', np.round(P_hi_q, 2), self.hot_refrigerant)

        try:
            # if math.isnan((float(self.hot_mass_flowrate.to('kg/s').m))):
            #     self.hot_mass_flowrate = (
            #         (self.process_heat_requirement.to('W') / (h_ho - h_hi)).to('kg/s'))

            if math.isnan((float(self.hot_mass_flowrate.to('kg/s').m))) and \
                    self.m_refrigerant == 'NaN':
                # self.hot_mass_flowrate = \
                #     (self.process_heat_requirement.to('W')/(h_ho - h_hi)).to('kg/s')
                self.hot_mass_flowrate = (
                    (self.process_heat_requirement.to('W') / (h_ho_new - h_hi_new)).to('kg/s'))
            elif self.m_refrigerant == 'NaN':
                # self.process_heat_requirement = \
                #     (self.hot_mass_flowrate.to('kg/s')*(h_ho - h_hi)).to('kW')
                self.process_heat_requirement = \
                    (self.hot_mass_flowrate.to('kg/s') * (h_ho_new - h_hi_new)).to('W')
            else:
                self.process_heat_requirement = self.pr_heat_rej
            # else:

            #     self.process_heat_requirement = (self.hot_mass_flowrate.to('kg/s') *
            #                                      (h_ho - h_hi)).to('W')
        except Exception:
            print('Provide either .hot_mass_flowrate or .process_heat_requirement.')
            quit()

        # Cold
        cold_dT = self.cold_buffer + self.cold_deltaT

        # h_ci = Q_(PropsSI('H', 'T',
        #                   self.cold_temperature_available.to('degK').m,
        #                   'P', self.cold_pressure.to('Pa').m,
        #                   self.cold_refrigerant), 'J/kg')
        h_ci_new = Q_(PropsSI('H', 'T',
                              self.cold_temperature_available.to('degK').m,
                              'Q', 0, self.cold_refrigerant),
                      'J/kg')
        P_ci_q = PropsSI('P', 'T',
                         self.cold_temperature_available.to('degK').m,
                         'Q', 0, self.hot_refrigerant)
        S_ci_new = PropsSI('S', 'H',
                           np.round(h_ci_new.to('J/kg').m, 2),
                           'P', np.round(P_ci_q, 2), self.hot_refrigerant)

        self.cold_final_temperature = self.cold_temperature_available - cold_dT
        # h_co = Q_(PropsSI('H', 'T',
        #                   self.cold_final_temperature.to('degK').m, 'P',
        #                   self.cold_pressure.to('Pa').m,
        #                   self.cold_refrigerant), 'J/kg')
        h_co_new = Q_(PropsSI('H', 'T',
                              self.cold_final_temperature.to('degK').m,
                              'Q', 0, self.cold_refrigerant),
                      'J/kg')
        P_co_q = PropsSI('P', 'T',
                         self.cold_final_temperature.to('degK').m,
                         'Q', 0, self.hot_refrigerant)
        S_co_new = PropsSI('S', 'H',
                           np.round(h_co_new.to('J/kg').m, 2), 'P',
                           np.round(P_co_q, 2), self.hot_refrigerant)
        if self.m_refrigerant != 'NaN':
            # self.cold_mass_flowrate = self.process_heat_requirement/(h_ci - h_co)
            self.cold_mass_flowrate = self.process_heat_requirement / (h_ci_new - h_co_new)
            # self.hot_mass_flowrate = self.process_heat_requirement/(h_ho - h_hi)
            self.hot_mass_flowrate_average = (self.process_heat_requirement / (h_ho_new - h_hi_new))
        else:
            self.cold_mass_flowrate = self.process_heat_requirement.to('W') / (h_ci_new - h_co_new)
            self.hot_mass_flowrate_average = np.mean(self.hot_mass_flowrate).to('kg /s')

        # # Calculating the Work into the heat pump
        # self.power_in = self.process_heat_requirement / self.actual_COP

        # Calculating the Work into the heat pump
        if self.m_refrigerant != 'NaN':
            self.power_in = self.process_heat_requirement / self.actual_COP
            # self.process_heat_requirement2 = float(self.process_heat_requirement)
        else:

            self.power_in = self.process_heat_requirement / self.actual_COP
            # self.process_heat_requirement2 = self.process_heat_requirement.to('W').m.item()
        # for i in range(0,8760):
        #    self.power_in[i] = self.process_heat_requirement_kw[i]/self.actual_COP
        self.average_power_in = np.mean(self.power_in)
        # self.annual_energy_in = self.mysum(self.power_in*Q_('1 hour')).to('kWh')

        # if (self.power_demand.m - self.average_power_in.m) > 10:
        #     print('all good')

        if self.print_results:
            print('Hot Mass Flow: {:~.3P}'.format(self.hot_mass_flowrate_average))
            print('Cold Mass Flow: {:~.3P}'.format(self.cold_mass_flowrate))
            print('Cold Outlet Temperature: {:~.2fP}'.format(self.cold_final_temperature))
            print('Cold Outlet Temperature: ', self.cold_final_temperature)
            # print('Thermal Demand: {:~.3fP}'.format(self.process_heat_requirement))
            print('Thermal Demand: ', self.process_heat_requirement)
            print('Power Draw of Heat Pump: {:~.3fP}'.format(self.power_in))

        self.water_cond_T = [float(self.hot_temperature_minimum.to('degK').m),
                             float(self.hot_temperature_desired.to('degK').m)]
        self.water_cond_P = [float(P_ho_q), float(P_hi_q)]
        self.water_cond_S = [float(S_ho_new), float(S_hi_new)]

        self.water_evap_T = [float(self.cold_temperature_available.to('degK').m),
                             float(self.cold_final_temperature.to('degK').m)]
        self.water_evap_P = [float(P_ci_q), (P_co_q)]
        self.water_evap_S = [float(S_ci_new), float(S_co_new)]

    def run_simulation(self):
        self.calculate_COP()
        self.calculate_energy_and_mass_flow()
