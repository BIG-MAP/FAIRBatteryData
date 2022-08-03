classdef ManufacturedMaterialBatch < TraceableObject
    %MANUFACTUREDMATERIALBATCH Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        dateManufactured
        dateReceived
    end
    
    methods
        function obj = ManufacturedMaterialBatch()
            %MANUFACTUREDMATERIALBATCH Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

