# ===================================
# Ruby Fundamentals Demo Script
# ===================================

# 1. Variables and String Interpolation
puts "=== Variables & String Interpolation ==="
name = "John"
age = 30

puts "Hello #{name}"
puts "Next year you'll be #{age + 1}"
puts

# 2. Conditionals (if/elsif/else)
puts "=== Conditionals ==="
temperature = 18

if temperature > 25
  puts "It's hot outside! "
elsif temperature > 20
  puts "It's warm and pleasant"
elsif temperature > 10
  puts "It's cool - #{temperature}°C"
else
  puts "It's cold! "
end
puts

# 3. Loops and Blocks
puts "=== Loops & Iteration ==="
puts "Counting with .times:"
3.times do |i|
  puts "  #{i + 1}. Iteration number #{i}"
end

puts "\nIterating with .each:"
["Ruby", "Python", "JavaScript"].each do |lang|
  puts "  - #{lang}"
end

puts "\nRange iteration:"
(1..5).each { |num| puts "  Square of #{num} is #{num ** 2}" }
puts

# 4. Methods/Functions
puts "=== Methods ==="
def greet(name)
  "Hello, #{name}!"
end

def calculate_area(width, height)
  width * height
end

puts greet("Ruby Developer")
puts "Area of 5x3 rectangle: #{calculate_area(5, 3)} sq units"
puts

# 5. Arrays and Hashes
puts "=== Collections ==="
fruits = ["apple", "banana", "cherry"]
puts "Fruits: #{fruits.join(', ')}"
puts "First fruit: #{fruits.first}"
puts "Last fruit: #{fruits.last}"

person = { name: "Alice", age: 28, role: "Developer" }
puts "\nPerson info:"
person.each { |key, value| puts "  #{key.capitalize}: #{value}" }
puts

# 6. User Input (Interactive)
puts "=== Interactive Input ==="
puts "What is your name?"
user_name = gets.chomp

puts "How old are you?"
user_age = gets.chomp.to_i

puts "\nNice to meet you, #{user_name}!"
puts "In 10 years, you'll be #{user_age + 10} years old."
