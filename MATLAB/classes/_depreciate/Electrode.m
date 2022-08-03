classdef Electrode < TraceableObject
    %ELECTRODE Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        ActiveMaterial
        Binder
        Additive
        CurrentCollector

        massLoading
        coatingThickness
        coatingSides
        porosity
        tortuosity
        length
        width

    end
    
    methods
        function obj = Electrode()
            %ELECTRODE Construct an instance of this class
            %   Detailed explanation goes here
            obj.ActiveMaterial = ActiveMaterial();
            obj.Binder = Binder();
            obj.CurrentCollector = CurrentCollector();
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

