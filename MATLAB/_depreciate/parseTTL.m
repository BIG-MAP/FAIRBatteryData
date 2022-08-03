clear all
close all
clc

file = 'C:\Users\simonc\Documents\GitHub\BattINFO\battery.ttl';
fid = fopen(file);

class_definition_lines = [];
class_section = 0;
class = OntologyClass();

line_no = 1;
count = 0;
prefix_count = 1;
prefix_key_set = {};
prefix_value_set = {};
while ~feof(fid)
    line = fgetl(fid);

    % create @prefix key-value pairs
    if ~isempty(regexp(line, '@prefix', 'once'))
        pos0  = find(line == ' ');
        pos1 = find(line == '<');
        pos2 = find(line == '>'); 
        prefix_key_set{end+1} = line(pos0(1)+1:pos0(2)-1);
        prefix_value_set{end+1} = line(pos1+1:pos2-1);  
    end

    % make a prefix map object when the end of the @prefix section is
    % reached
    if ~isempty(regexp(line, '@base', 'once'))
        prefix = containers.Map(prefix_key_set,prefix_value_set);
    end

    % identify when the class section has started
    if ~isempty(regexp(line, '#    Classes', 'once'))
        class_section = 1;
    end

    % identify when a new class definition starts
    if ~isempty(regexp(line, '###  http', 'once')) && class_section == 1
%         class_definition_lines(end+1) = line_no;
        if isempty(class(1).iri)
            class(1) = OntologyClass(line(6:end));
        else
            class(end+1) = OntologyClass(line(6:end));
        end
        % iterate through the class definition lines and assign properties
        while ~isempty(line) && ~feof(fid)
            line = fgetl(fid);
            % identify the prefLabel
            if ~isempty(regexp(line, 'prefLabel', 'once'))
                pos = find(line == '"');
                class(end).prefLabel = convertCharsToStrings(line(pos(1)+1:pos(2)-1));

            % identify the altLabel
            elseif ~isempty(regexp(line, 'altLabel', 'once'))
                pos = find(line == '"');
                class(end).altLabel = convertCharsToStrings(line(pos(1)+1:pos(2)-1));
                while line(end) ~= ';'
                    line = fgetl(fid);
                    pos = find(line == '"');
                    class(end).altLabel(end+1) = convertCharsToStrings(line(pos(1)+1:pos(2)-1));
                end

            % identify the elucidation
            elseif ~isempty(regexp(line, 'EMMO_967080e5_2f42_4eb2_a3a9_c58143e835f9', 'once'))
                pos = find(line == '"');
                class(end).elucidation = convertCharsToStrings(line(pos(1)+1:pos(2)-1));

            % identify the comments
            elseif ~isempty(regexp(line, 'rdfs:comment', 'once'))
                pos = find(line == '"');
                class(end).comment = convertCharsToStrings(line(pos(1)+1:pos(2)-1));
                while line(end) ~= ';'
                    line = fgetl(fid);
                    pos = find(line == '"');
                    class(end).comment(end+1) = convertCharsToStrings(line(pos(1)+1:pos(2)-1));
                end
                
            % identify the subclass definitions
            elseif ~isempty(regexp(line, 'subClassOf', 'once'))
                pos = strfind(line, 'subClassOf');
                len = length('subClassOf');
                value = line(pos+len+1:end-2);
                % identify if a prefix is present
                is_found = 0;
                ind = 0;
                while is_found == 0 && ind <= length(prefix_key_set)-1
                %for ind = 0:length(prefix_key_set)-1
                    if ~isempty(strfind(value, prefix_key_set{end-ind}))
                        found = prefix_key_set{end-ind};
                        value(1:length(found)) = [];
                        value = convertCharsToStrings(strcat(prefix(found), value));
                        is_found = 1;
                    end
                    ind = ind + 1;
                end
                class(end).is_a = value;
                while line(end) ~= ';'
                    line = fgetl(fid);
                    if ~contains(line, '[')
                        pos0 = find(line~=' ');
                        value = line(pos0(1):end-2);
                        % identify if a prefix is present
                        is_found = 0;
                        ind = 0;
                        while is_found == 0 && ind <= length(prefix_key_set)-1
                        %for ind = 0:length(prefix_key_set)-1
                            if ~isempty(strfind(value, prefix_key_set{end-ind}))
                                found = prefix_key_set{end-ind};
                                value(1:length(found)) = [];
                                value = convertCharsToStrings(strcat(prefix(found), value));
                                is_found = 1;
                            end
                            ind = ind + 1;
                        end
                        class(end).is_a(end+1) = value;
                    end
                end
                 
                
            end
        end
    end
%     line_no = line_no + 1;
end
   
