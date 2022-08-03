classdef DataModel < dynamicprops
    %UNTITLED9 Summary of this class goes here
    %   Detailed explanation goes here

    properties
        meta
        description        
    end

    methods
        function obj = DataModel(filename)
            %UNTITLED9 Construct an instance of this class
            %   Detailed explanation goes here

            % read and parse the DLite data model
            temp = parsedlitemeta(filename);
            
            % write general identifing header information
            obj.meta = [temp.namespace, '/', temp.version, '/', temp.name];
            obj.description = temp.description;
            
            % iterate over the properties in the DLite data model and add
            % them to the MATLAB class
            for ind = 1:length(temp.properties)
                % check if there is more than one property defined and
                % extract the current property
                if ~(length(temp.properties)==1)
                    prop = temp.properties{ind};
                else
                    prop = temp.properties;
                end
                propname = prop.name;
                % check if the property references another data model and
                % assign appropriately
                if strcmpi(prop.type, 'ref')
                    addprop(obj, propname);
                    metadata_path = regexp(prop.x_ref,'/','split');
                    metadata_filename = [metadata_path{end}, '.json'];
                    obj.(propname) = DataModel(metadata_filename);
                else
                    addprop(obj, propname);
                end
            end

            % generate a uuid if there is such a property
            if isprop(obj,'uuid')
                obj.generateuuid;
            end
        end

        function load(obj, filename)

            % parse the JSON file as a MATLAB structure
            data = parseJson(filename);

            % populate the properties of the data model with values from
            % the loaded profile.
            obj.populate(data);
            
        end

        function populate(obj, data)

            % get the fieldnames of the data structure
            fieldnames = fields(data);

            % iterate over all of the fieldnames
            for ind = 1:length(fieldnames)
                % check if the field contains a structure and sub-populate
                % it. Else, assign the value from the data structure to the
                % associated class property.
                if isstruct(data.(fieldnames{ind}))
                    % check if there are multiple structures in the field
                    if length(data.(fieldnames{ind})) > 1
                        for ind2 = 1:length(data.(fieldnames{ind}))
                            metadata_path = regexp(obj.(fieldnames{ind}).meta,'/','split');
                            metadata_filename = [metadata_path{end}, '.json'];
                            obj.(fieldnames{ind})(ind2) = DataModel(metadata_filename);
                            H = obj.(fieldnames{ind})(ind2);
                            subdata = data.(fieldnames{ind})(ind2);
                            H.populate(subdata);
                        end
                    else
                        H = obj.(fieldnames{ind});
                        subdata = data.(fieldnames{ind});
                        H.populate(subdata);
                    end
                elseif ~isempty(data.(fieldnames{ind}))
                    obj.(fieldnames{ind}) = data.(fieldnames{ind});
                end
            end

        end

        function tables = createTable(obj)

            tables{1} = table();

            % get the fieldnames of the data structure
            propnames = properties(obj);
            metadata_path = regexp(obj.meta,'/','split');
            table_name = metadata_path{end};


            % iterate over all of the fieldnames
            for ind = 1:length(propnames)
                % check if the field contains a structure and sub-populate
                % it. Else, assign the value from the data structure to the
                % associated class property.
                if isa(obj.(propnames{ind}), 'DataModel')
                    % check if there are multiple structures in the field
%                     if length(data.(propnames{ind})) > 1
%                         for ind2 = 1:length(data.(propnames{ind}))
%                             metadata_path = regexp(obj.(propnames{ind}).meta,'/','split');
%                             metadata_filename = [metadata_path{end}, '.json'];
%                             obj.(propnames{ind})(ind2) = DataModel(metadata_filename);
%                             H = obj.(propnames{ind})(ind2);
%                             subdata = data.(propnames{ind})(ind2);
%                             H.populate(subdata);
%                         end
%                     else
                        H = obj.(propnames{ind});
                        tables{end+1} = H.createTable();
                    
                else
                    tables{end}.(propnames{ind}) = 'NULL';
                end
            end
%             tables{end+1} = table();

        end

        function generateuuid(obj)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            if ~isempty(obj.uuid)
                msg = "You are overwriting a UUID.";
                warning(msg)
            end
            obj.uuid =  string(java.util.UUID.randomUUID);
        end
    end
end