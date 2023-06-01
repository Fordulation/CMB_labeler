function []=hello_world_matlab(first_argument, second_argument);

% Check that the arguments are both there.
if exist('second_argument') ~= 1 || exist('second_argument') ~= 1
    disp('ERROR: Not enough input arguments');
    return
end
disp(sprintf('Hello World! First argument was |%s|. Second argument was |%s|.', first_argument, second_argument))
