classdef OntologyClass < handle
    %ONTOLOGYCLASS Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        iri = string()
        prefLabel
        altLabel
        elucidation
        comment
        is_a
    end
    
    methods
        function obj = OntologyClass(varargin)
            %ONTOLOGYCLASS Construct an instance of this class
            %   Detailed explanation goes here
            if ~isempty(nargin)
                obj.iri = convertCharsToStrings(varargin);
            end
        end
        
    end
end

