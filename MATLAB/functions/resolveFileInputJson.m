function jsonstruct = resolveFileInputJson(jsonstruct)
    
%     fileroot = fileparts(which('playFAIR.m'));
%     fileroot = [fileroot, '\examples\entities\profiles\'];
    
    if isstruct(jsonstruct)
        fds = fieldnames(jsonstruct);
        if ismember('isFile', fds)
            filename = jsonstruct.filename;
            fullfilename = [fileparts(which(filename)), '\', jsonstruct.filename];
            jsonsrc = fileread(fullfilename);
            parsedjson = jsondecode(jsonsrc);
            jsonstruct = parsedjson;
        end
        fds = fieldnames(jsonstruct);
        for ind = 1 : numel(fds)
            if isstruct(jsonstruct.(fds{ind})) && length(jsonstruct.(fds{ind})) >=2
                temp = jsonstruct.(fds{ind});
                jsonstruct.(fds{ind}) = [];
                for ind2 = 1:length(temp)
                    if ind2 == 1
                        jsonstruct.(fds{ind}) = resolveFileInputJson(temp(ind2));
                    else
                        jsonstruct.(fds{ind})(ind2) = resolveFileInputJson(temp(ind2));
                    end
                end
            else
                jsonstruct.(fds{ind}) = resolveFileInputJson(jsonstruct.(fds{ind}));
            end
            
        end
    end
    
end



%{
Copyright 2009-2021 SINTEF Industry, Sustainable Energy Technology
and SINTEF Digital, Mathematics & Cybernetics.

This file is part of The Battery Modeling Toolbox BattMo

BattMo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BattMo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BattMo.  If not, see <http://www.gnu.org/licenses/>.
%}
