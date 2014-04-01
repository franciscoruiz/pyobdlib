# pyobdlib
# Copyright (C) 2004 Donour Sizemore
# Copyright (C) 2009 Secons Ltd.
# Copyright (C) 2013 Mark Embling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from .conversion import *


class Sensor:

    def __init__(self, command, short_name, name, value_func=noop, unit=""):
        self.cmd = command
        self.shortname = short_name
        self.name = name
        self.value = value_func
        self.unit = unit


# Sensor definitions. Note that not all units/conversions appear to be
# implemented. Those which are not will return the raw hex value.
# More info: http://en.wikipedia.org/wiki/OBD-II_PIDs#Standard_PIDs
SENSORS = [
    Sensor("0100", "pids", "Supported PIDs", to_bitstring),
    Sensor("0101", "dtc_status", "Status Since DTC Cleared", dtc_decode),
    Sensor("0102", "dtc_ff", "DTC Causing Freeze Frame"),
    Sensor("0103", "fuel_status", "Fuel System Status"),
    Sensor("01041", "load", "Calculated Load Value", to_percent_scale, "%"),
    Sensor("0105", "temp", "Coolant Temperature", to_temp_c, "C"),
    Sensor("0106", "short_term_fuel_trim_1", "Short Term Fuel Trim", to_fuel_trim_percent, "%"),
    Sensor("0107", "long_term_fuel_trim_1", "Long Term Fuel Trim", to_fuel_trim_percent, "%"),
    Sensor("0108", "short_term_fuel_trim_2", "Short Term Fuel Trim", to_fuel_trim_percent, "%"),
    Sensor("0109", "long_term_fuel_trim_2", "Long Term Fuel Trim", to_fuel_trim_percent, "%"),
    Sensor("010A", "fuel_pressure", "Fuel Rail Pressure", to_kpa_gauge, "kPa"),
    Sensor("010B", "manifold_pressure", "Intake Manifold Pressure", to_int, "kPa"),
    Sensor("010C1", "rpm", "Engine RPM", to_rpm, "rpm"),
    Sensor("010D1", "speed", "Vehicle Speed", to_int, "km/h"),
    Sensor("010E", "timing_advance", "Timing Advance", to_timing_advance, "degrees"),
    Sensor("010F", "intake_air_temp", "Intake Air Temp", to_temp_c, "C"),
    Sensor("0110", "maf", "Air Flow Rate (MAF)", to_maf_grams_sec, "grams/sec"),
    Sensor("01111", "throttle_pos", "Throttle Position", to_percent_scale, "%"),
    Sensor("0112", "secondary_air_status", "Secondary Air Status"),
    Sensor("0113", "o2_sensor_positions", "Location of O2 sensors"),
    Sensor("0114", "o211", "O2 Sensor: 1 - 1", to_fuel_trim_percent, "%"),
    Sensor("0115", "o212", "O2 Sensor: 1 - 2", to_fuel_trim_percent, "%"),
    Sensor("0116", "o213", "O2 Sensor: 1 - 3", to_fuel_trim_percent, "%"),
    Sensor("0117", "o214", "O2 Sensor: 1 - 4", to_fuel_trim_percent, "%"),
    Sensor("0118", "o221", "O2 Sensor: 2 - 1", to_fuel_trim_percent, "%"),
    Sensor("0119", "o222", "O2 Sensor: 2 - 2", to_fuel_trim_percent, "%"),
    Sensor("011A", "o223", "O2 Sensor: 2 - 3", to_fuel_trim_percent, "%"),
    Sensor("011B", "o224", "O2 Sensor: 2 - 4", to_fuel_trim_percent, "%"),
    Sensor("011C", "obd_standard", "OBD Designation"),
    Sensor("011D", "o2_sensor_position_b", "Location of O2 sensors"),
    Sensor("011E", "aux_input", "Aux input status"),
    Sensor("011F", "engine_time", "Time Since Engine Start", to_int, "secs"),
    Sensor("0120", "pids2", "PIDs_supported_[21_-_40]", to_bitstring),
    Sensor("0121", "Distance_traveled_with_", "Distance_traveled_with_m"),
    Sensor("0122", "Fuel_Rail_Pressure_(rel", "Fuel_Rail_Pressure_(rela"),
    Sensor("0123", "Fuel_Rail_Pressure_(die", "Fuel_Rail_Pressure_(dies"),
    Sensor("0124", "O2S1_WR_lambda", "O2S1_WR_lambda(1)"),
    Sensor("0125", "O2S2_WR_lambda", "O2S2_WR_lambda(1)"),
    Sensor("0126", "O2S3_WR_lambda", "O2S3_WR_lambda(1)"),
    Sensor("0127", "O2S4_WR_lambda", "O2S4_WR_lambda(1)"),
    Sensor("0128", "O2S5_WR_lambda", "O2S5_WR_lambda(1)"),
    Sensor("0129", "O2S6_WR_lambda", "O2S6_WR_lambda(1)"),
    Sensor("012A", "O2S7_WR_lambda", "O2S7_WR_lambda(1)"),
    Sensor("012B", "O2S8_WR_lambda", "O2S8_WR_lambda(1)"),
    Sensor("012C", "Commanded_EGR", "Commanded_EGR"),
    Sensor("012D", "EGR_Error", "EGR_Error"),
    Sensor("012E", "Commanded_evaporative_p", "Commanded_evaporative_pu"),
    Sensor("012F", "Fuel_Level_Input", "Fuel_Level_Input"),
    Sensor("0130", "of_warm-ups_since_cod", "of_warm-ups_since_code"),
    Sensor("0131", "Distance_traveled_since", "Distance_traveled_since_"),
    Sensor("0132", "Evap._System_Vapor_Pres", "Evap._System_Vapor_Press"),
    Sensor("0133", "Barometric_pressure", "Barometric_pressure"),
    Sensor("0134", "O2S1_WR_lambda", "O2S1_WR_lambda(1)"),
    Sensor("0135", "O2S2_WR_lambda", "O2S2_WR_lambda(1)"),
    Sensor("0136", "O2S3_WR_lambda", "O2S3_WR_lambda(1)"),
    Sensor("0137", "O2S4_WR_lambda", "O2S4_WR_lambda(1)"),
    Sensor("0138", "O2S5_WR_lambda", "O2S5_WR_lambda(1)"),
    Sensor("0139", "O2S6_WR_lambda", "O2S6_WR_lambda(1)"),
    Sensor("013A", "O2S7_WR_lambda", "O2S7_WR_lambda(1)"),
    Sensor("013B", "O2S8_WR_lambda", "O2S8_WR_lambda(1)"),
    Sensor("013C", "Catalyst_Temperature", "Catalyst_Temperature"),
    Sensor("013D", "Catalyst_Temperature", "Catalyst_Temperature"),
    Sensor("013E", "Catalyst_Temperature", "Catalyst_Temperature"),
    Sensor("013F", "Catalyst_Temperature", "Catalyst_Temperature"),
    Sensor("0140", "pids3", "PIDs_supported_[41_-_60]", to_bitstring),
    Sensor("0141", "Monitor_status_this_dri", "Monitor_status_this_driv"),
    Sensor("0142", "Control_module_voltage", "Control_module_voltage"),
    Sensor("0143", "Absolute_load_value", "Absolute_load_value"),
    Sensor("0144", "Command_equivalence_rat", "Command_equivalence_rati"),
    Sensor("0145", "Relative_throttle_posit", "Relative_throttle_positi"),
    Sensor("0146", "Ambient_air_temperature", " Ambient_air_temperature"),
    Sensor("0147", "Absolute_throttle_posit", "Absolute_throttle_positi"),
    Sensor("0148", "Absolute_throttle_posit", "Absolute_throttle_positi"),
    Sensor("0149", "Accelerator_pedal_posit", "Accelerator_pedal_positi"),
    Sensor("014A", "Accelerator_pedal_posit", "Accelerator_pedal_positi"),
    Sensor("014B", "Accelerator_pedal_posit", "Accelerator_pedal_positi"),
    Sensor("014C", "Commanded_throttle_actu", "Commanded_throttle_actua"),
    Sensor("014D", "Time_run_with_MIL_on", "Time_run_with_MIL_on"),
    Sensor("014E", "Time_since_trouble_code", "Time_since_trouble_codes"),
    Sensor("014F", "Maximum_value_for_equiv", "Maximum_value_for_equiva"),
    Sensor("0150", "Maximum_value_for_air_f", "Maximum_value_for_air_fl"),
    Sensor("0151", "Fuel_Type", "Fuel_Type"),
    Sensor("0152", "Ethanol_fuel_%", "Ethanol_fuel_%"),
    Sensor("0153", "Absolute_Evap_system_Va", "Absolute_Evap_system_Vap"),
    Sensor("0154", "Evap_system_vapor_press", "Evap_system_vapor_pressu"),
    Sensor("0155", "Short_term_secondary_ox", "Short_term_secondary_oxy"),
    Sensor("0156", "Long_term_secondary_oxy", "Long_term_secondary_oxyg"),
    Sensor("0157", "Short_term_secondary_ox", "Short_term_secondary_oxy"),
    Sensor("0158", "Long_term_secondary_oxy", "Long_term_secondary_oxyg"),
    Sensor("0159", "Fuel_rail_pressure_(abs", "Fuel_rail_pressure_(abso"),
    Sensor("015A", "Relative_accelerator_pe", "Relative_accelerator_ped"),
    Sensor("015B", "Hybrid_battery_pack_rem", "Hybrid_battery_pack_rema"),
    Sensor("015C", "Engine_oil_temperature", "Engine_oil_temperature"),
    Sensor("015D", "Fuel_injection_timing", "Fuel_injection_timing"),
    Sensor("015E", "Engine_fuel_rate", "Engine_fuel_rate"),
    Sensor("015F", "Emission_requirements_t", "Emission_requirements_to"),
    Sensor("0160", "pids4", "PIDs_supported_[61_-_80]", to_bitstring),
    Sensor("0161", "Driver's_demand_engine_", "Driver's_demand_engine_-"),
    Sensor("0162", "Actual_engine_-_percent", "Actual_engine_-_percent_"),
    Sensor("0163", "Engine_reference_torque", "Engine_reference_torque"),
    Sensor("0164", "Engine_percent_torque_d", "Engine_percent_torque_da"),
    Sensor("0165", "Auxiliary_input_/_outpu", "Auxiliary_input_/_output"),
    Sensor("0166", "Mass_air_flow_sensor", "Mass_air_flow_sensor"),
    Sensor("0167", "Engine_coolant_temperat", "Engine_coolant_temperatu"),
    Sensor("0168", "Intake_air_temperature_", "Intake_air_temperature_s"),
    Sensor("0169", "Commanded_EGR_and_EGR_E", "Commanded_EGR_and_EGR_Er"),
    Sensor("016A", "Commanded_Diesel_intake", "Commanded_Diesel_intake_"),
    Sensor("016B", "Exhaust_gas_recirculati", "Exhaust_gas_recirculatio"),
    Sensor("016C", "Commanded_throttle_actu", "Commanded_throttle_actua"),
    Sensor("016D", "Fuel_pressure_control_s", "Fuel_pressure_control_sy"),
    Sensor("016E", "Injection_pressure_cont", "Injection_pressure_contr"),
    Sensor("016F", "Turbocharger_compressor", "Turbocharger_compressor_"),
    Sensor("0170", "Boost_pressure_control", "Boost_pressure_control"),
    Sensor("0171", "Variable_Geometry_turbo", "Variable_Geometry_turbo_"),
    Sensor("0172", "Wastegate_control", "Wastegate_control"),
    Sensor("0173", "Exhaust_pressure", "Exhaust_pressure"),
    Sensor("0174", "Turbocharger_RPM", "Turbocharger_RPM"),
    Sensor("0175", "Turbocharger_temperatur", "Turbocharger_temperature"),
    Sensor("0176", "Turbocharger_temperatur", "Turbocharger_temperature"),
    Sensor("0177", "Charge_air_cooler_tempe", "Charge_air_cooler_temper"),
    Sensor("0178", "Exhaust_Gas_temperature", "Exhaust_Gas_temperature_"),
    Sensor("0179", "Exhaust_Gas_temperature", "Exhaust_Gas_temperature_"),
    Sensor("017A", "Diesel_particulate_filt", "Diesel_particulate_filte"),
    Sensor("017B", "Diesel_particulate_filt", "Diesel_particulate_filte"),
    Sensor("017C", "Diesel_Particulate_filt", "Diesel_Particulate_filte"),
    Sensor("017D", "NOx_NTE_control_area_st", "NOx_NTE_control_area_sta"),
    Sensor("017E", "PM_NTE_control_area_sta", "PM_NTE_control_area_stat"),
    Sensor("017F", "Engine_run_time", "Engine_run_time"),
    Sensor("0180", "pids5", "PIDs_supported_[81_-_A0]", to_bitstring),
    Sensor("0181", "Engine_run_time_for_Aux", "Engine_run_time_for_Auxi"),
    Sensor("0182", "Engine_run_time_for_Aux", "Engine_run_time_for_Auxi"),
    Sensor("0183", "NOx_sensor", "NOx_sensor"),
    Sensor("0184", "Manifold_surface_temper", "Manifold_surface_tempera"),
    Sensor("0185", "NOx_reagent_system" , "NOx_reagent_system"),
    Sensor("0186", "Particulate_matter_(PM)", "Particulate_matter_(PM)_"),
    Sensor("0187", "Intake_manifold_absolut", "Intake_manifold_absolute"),
]
