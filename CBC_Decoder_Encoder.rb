require 'base64'
require 'uri'
# Used for pentxsterlab chall 
# Decode a URL-encoded string and then decode the Base64 content
def decode_string(encoded_str)
  # URL decode
  url_decoded = URI.decode_www_form_component(encoded_str)
  # Base64 decode
  base64_decoded = Base64.decode64(url_decoded)
  base64_decoded
end

# Encode a string by Base64 encoding and then URL encoding
def encode_string(str)
  # Base64 encode
  base64_encoded = Base64.encode64(str)
  # URL encode
  url_encoded = URI.encode_www_form_component(base64_encoded)
  url_encoded
end

# Prompt user for action
puts "What would you like to do? (1: Encode, 2: Decode)"
choice = gets.chomp.to_i

# Prompt user for the string to process
puts "Enter the string:"
input_str = gets.chomp

if choice == 1
  # Encode the string
  encoded_str = encode_string(input_str)
  puts "Encoded string: #{encoded_str}"
elsif choice == 2
  # Decode the string
  decoded_str = decode_string(input_str)
  puts "Decoded string: #{decoded_str.inspect}"
else
  puts "Invalid choice. Please enter 1 for Encode or 2 for Decode."
end




