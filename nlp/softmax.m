function[prob] = softmax(z)
  values = e .^ z;
  denom = diag(sum(values, 2) .^ -1);
  prob = denom * values;
end
