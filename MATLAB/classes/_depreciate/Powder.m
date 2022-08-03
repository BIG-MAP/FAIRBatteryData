classdef Powder < ManufacturedMaterial
    %POWDER Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        particleSizeDistribution
        specificSurfaceArea
    end
    
    methods
        function obj = Powder()
            %POWDER Construct an instance of this class
            %   Detailed explanation goes here
            
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

