function metadataModel = createMetadataModel(filename)
%UNTITLED7 Summary of this function goes here
%   Detailed explanation goes here

% read and parse the DLite data model
temp = parsedlitemeta(filename);

% write general identifing header information
metadataModel.meta = [temp.namespace, '/', temp.version, '/', temp.name];
metadataModel.description = temp.description;
metadataModel.properties = struct();

for ind = 1:length(temp.properties)
    propname = temp.properties{ind}.name;
    if strcmpi(temp.properties{ind}.type, 'ref')
        metadataModel.properties.(propname) = struct();
        metadata_path = regexp(temp.properties{ind}.x_ref,'/','split');
        metadata_filename = [metadata_path{end}, '.json'];
        metadataModel.properties.(propname) = createMetadataModel(metadata_filename);
    else
        metadataModel.properties.(propname) = [];
    end
end

end