classdef CurrentCollector < TraceableObject
    %CURRENTCOLLECTOR Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        Material
        thickness
        length
        width
    end
    
    methods
        function obj = CurrentCollector()
            %CURRENTCOLLECTOR Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

