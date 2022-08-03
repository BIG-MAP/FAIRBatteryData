classdef BatteryCell < TraceableObject
    %BATTERYCELL Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        NegativeElectrode
        PositiveElectrode
        Electrolyte
        Separator
        Casing

        nominalCapacity
        nominalVoltage
        chargingVoltage
        maxChargingCurrent
    end
    
    methods
        function obj = BatteryCell()
            %BATTERYCELL Construct an instance of this class
            %   Detailed explanation goes here
            obj.NegativeElectrode = Electrode();
            obj.PositiveElectrode = Electrode();
            obj.Electrolyte = ElectrolyteSolution();
            obj.Separator = Separator();
            obj.Casing = Casing();
            
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

