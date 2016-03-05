class ExError < StandardError
end


throw ExError.new('s')

