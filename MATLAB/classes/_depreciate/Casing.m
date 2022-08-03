classdef Casing < TraceableObject
    %CASING Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        length
        width
        height
        wallThickness
        formFactor
    end
    
    methods
        function obj = Casing()
            %CASING Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

