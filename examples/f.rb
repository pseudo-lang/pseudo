def f
  ''
end

puts f
begin
  2
  f
rescue StandardError => e
  puts e
end


