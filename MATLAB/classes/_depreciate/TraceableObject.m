classdef TraceableObject < handle
    %TRACEABLEOBJECT Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        uuid
        name
        mass
        volume
    end
    
    methods
        function obj = TraceableObject()
            %TRACEABLEOBJECT Construct an instance of this class
            %   Detailed explanation goes here
            obj.generateUUID();

        end
        
        function generateUUID(obj)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            obj.uuid =  string(java.util.UUID.randomUUID);
        end
    end
end

