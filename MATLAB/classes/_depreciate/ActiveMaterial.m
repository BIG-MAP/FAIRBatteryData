classdef ActiveMaterial < Powder
    %ACTIVEMATERIAL Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        theta0
        theta100
    end
    
    methods
        function obj = ActiveMaterial()
            %ACTIVEMATERIAL Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

