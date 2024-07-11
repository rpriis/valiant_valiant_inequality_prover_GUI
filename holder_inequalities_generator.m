

%% Generates NUM_INEQUALITIES BOUND-dimensional Holder Inequalities

format rational



my_points = '';
num_dims = 12;
BOUND = 2; % fit points into square [-BOUND, BOUND] x [-BOUND, BOUND]
NUM_INEQUALITIES = 5; % number of desired inequalities

i = 0

while i < NUM_INEQUALITIES
    divs = randi([-2, 2], 1, num_dims*2) ./ randi([1, 4], 1, num_dims*2);
    

    p_numerator = randi([2, 5], 1, 1);
    p_denominator = randi([1, p_numerator-1], 1, 1);
    p = p_numerator/p_denominator;
    
    q = p/(p-1);
    z = 1;
    
    
    first_terms = divs(1:num_dims);
    second_terms = divs(num_dims+1:2*num_dims);

    first_expression = [first_terms*p 1/p*z];
    second_expression = [second_terms*q 1/q*z];
    third_expression = [zeros(1, num_dims), -z];

    should_break = false;
    for j = 1:(num_dims)
        third_expression(j) = first_terms(j) + second_terms(j);

        if abs(first_expression(j)) > BOUND || abs(second_expression(j)) > BOUND || abs(third_expression(j)) > 1
            should_break = true;
            break
        end
    end
    if should_break
        continue % ignore these results
    end

    

    first_expr_string = '';
    second_expr_string = '';
    third_expr_string = '';

    for j = 1:(num_dims)
        first_expr_string = append(first_expr_string, sprintf('%s, ', strtrim(rats(first_expression(j)))));
        second_expr_string = append(second_expr_string, sprintf('%s, ', strtrim(rats(second_expression(j)))));
        third_expr_string = append(third_expr_string, sprintf('%s, ', strtrim(rats(third_expression(j)))));
    end
    first_expr_string = append(first_expr_string, sprintf('%s', strtrim(rats(first_expression(num_dims+1)))));
    second_expr_string = append(second_expr_string, sprintf('%s', strtrim(rats(second_expression(num_dims+1)))));
    third_expr_string = append(third_expr_string, sprintf('%s', strtrim(rats(third_expression(num_dims+1)))));

    new_string = append(first_expr_string, '; ', second_expr_string, '; ', third_expr_string, '; ');
    %new_string = sprintf('%s, %s, %s; %s, %s, %s; %s, %s, %s;', strtrim(rats(a)), strtrim(rats(b)), strtrim(rats(c)), strtrim(rats(d)), strtrim(rats(e)), strtrim(rats(f)), strtrim(rats(g)), strtrim(rats(h)), strtrim(rats(i)));

    my_points = append(my_points, new_string);


    i = i+1;
end


fprintf('[%s]\n', my_points)





