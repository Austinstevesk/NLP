function[density] = normal(z)
  density = (1 / (sqrt(2 * pi))) * (e .^ (-0.5 .* z .^ 2));
end
