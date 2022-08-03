classdef myDynamicClass < dynamicprops
    properties (Hidden)
        myClass %# this stores the class name
    end

    methods
        function obj = myDynamicClass(myClassName,varargin)
        %# synopsis: obj = myDynamicClass(myClassName,propertyName,propertyValue,...)
        %# myClassName is the name of the class that is returned by 'classname(obj)'
        %# propertyName/propertyValue define the dynamic properties
        
            obj.myClass = myClassName;
        
            for i=1:2:length(varargin)
                addprop(obj,varargin{i})
                obj.(varargin{i}) = varargin{i+1};
            end
        end
        
        function out = classname(obj)
            out = obj.myClass;
        end
    
    end 
end