import hashlib

# Hashovací funkce (MD5)
def hash_function(value):
    return hashlib.md5(value.encode()).hexdigest()

# Redukční funkce
def reduce_function(hash_value, position):
    length = len(hash_value)
    chars = []
    for i in range(4):
        start_index = (position + i * 2) % length
        end_index = start_index + 2
        part = hash_value[start_index:end_index]
        chars.append(chr(int(part, 16) % 26 + 97))
    return ''.join(chars)

# Generování Rainbow tabulek
def generate_rainbow_table(words, chain_length):
    rainbow_table = {}
    for word in words:
        start_value = word
        current_value = start_value
        
        for j in range(chain_length):
            hashed_value = hash_function(current_value)
            current_value = reduce_function(hashed_value, j)
        
        rainbow_table[current_value] = start_value
    
    return rainbow_table

# Příkladová slova
words = ["test", "hello", "world", "rainbow", "admin", "password"]

# Generování tabulky
rainbow_table = generate_rainbow_table(words, chain_length=2000)
print("Vygenerovaná Rainbow Tabulka:")
print(rainbow_table)


# Vyhledávání v Rainbow tabulce
def search_rainbow_table(hash_to_crack, chain_length, rainbow_table):
    for i in range(chain_length):
        current_hash = hash_to_crack
        for j in range(chain_length - i):
            reduced_value = reduce_function(current_hash, j)
            current_hash = hash_function(reduced_value)
        
        if reduced_value in rainbow_table:
            start_value = rainbow_table[reduced_value]
            current_value = start_value
            
            for j in range(chain_length):
                if hash_function(current_value) == hash_to_crack:
                    return current_value
                current_value = reduce_function(hash_function(current_value), j)
    
    return None

# Testování vyhledávání
hash_to_crack = hash_function('admin')
print(f'Hledaný hash: {hash_to_crack}')
cracked_value = search_rainbow_table(hash_to_crack, chain_length=2000, rainbow_table=rainbow_table)
print(f'Nalezená hodnota: {cracked_value}')
