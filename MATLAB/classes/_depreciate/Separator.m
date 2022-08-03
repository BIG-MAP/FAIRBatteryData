classdef Separator < TraceableObject
    %SEPARATOR Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        Material
        thickness
        length
        width
    end
    
    methods
        function obj = Separator()
            %SEPARATOR Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

