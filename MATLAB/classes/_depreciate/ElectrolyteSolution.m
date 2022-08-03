classdef ElectrolyteSolution < ManufacturedMaterial
    %ELECTROLYTESOLUTION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        density
        viscosity
        concentration
    end
    
    methods
        function obj = ElectrolyteSolution()
            %ELECTROLYTESOLUTION Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

