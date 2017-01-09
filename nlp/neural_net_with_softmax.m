function [J, grad] = neural_net_with_softmax(theta, input_layer, hidden_layer, num_labels, a1, y, lambda)
  m = size(a1, 1);
  s1 = [hidden_layer , input_layer+1];
  s2 = [num_labels , hidden_layer+1];
  theta1 = reshape(theta(1:prod(s1)), s1);
  theta2 = reshape(theta(prod(s1)+1:end), s2);

a2 = [ones(m,1) softmax(a1 * transpose(theta1))];

  a3 = softmax(a2 * transpose(theta2));

  %J = 1/m * sum(sum(-y .* log(a3) - (1 - y) .* log(1 - a3),2)) + lambda / (2 * m) * sum([theta1(:, 2:end)(:); theta2(:, 2:end)(:)] .^ 2);
  J = -sum(sum(y .* log(a3), 2)) + lambda / (2 * m) * sum([theta1(:, 2:end)(:); theta2(:, 2:end)(:)] .^ 2);

  l3 = (a3 - y);
l2 = l3 * theta2 .* (a2 .* (1 - a2));
	    
  g2 = transpose(l3) * a2;
  g1 = transpose(l2(:, 2:end)) * a1;
  g2 = [g2(:, 1) (g2(:, 2:end) .+ (lambda/m * theta2(:, 2:end)))];
  g1 = [g1(:, 1) (g1(:, 2:end) .+ (lambda/m * theta1(:, 2:end)))];

  grad = 1/m * [g1(:); g2(:)];

end
