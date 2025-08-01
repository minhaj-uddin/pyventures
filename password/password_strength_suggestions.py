import re


def check_password_strength(password):
    strength = 0

    # Check password length
    if len(password) >= 8:
        strength += 1
    # Check for lowercase letters
    if re.search('[a-z]', password):
        strength += 1
    # Check for uppercase letters
    if re.search('[A-Z]', password):
        strength += 1
    # Check for digits
    if re.search('[0-9]', password):
        strength += 1
    # Check for special characters
    if re.search('[@#$%+=!]', password):
        strength += 1

    return strength


def provide_suggestions(strength, password):
    suggestions = []

    # If password is too weak, suggest improvements
    if len(password) < 8:
        suggestions.append(
            "Add more characters to your password (at least 8).")
    if not re.search('[a-z]', password):
        suggestions.append("Include at least one lowercase letter.")
    if not re.search('[A-Z]', password):
        suggestions.append("Include at least one uppercase letter.")
    if not re.search('[0-9]', password):
        suggestions.append("Include at least one number.")
    if not re.search('[@#$%+=!]', password):
        suggestions.append(
            "Include at least one special character (e.g., @, #, $, %, +).")

    # Provide advice for very weak passwords
    if strength < 3:
        suggestions.append(
            "Avoid using easily guessable information, such as names or common words.")

    if not suggestions:
        suggestions.append("Your password is quite strong! Keep it up.")

    return suggestions


def main():
    password = input('Enter a password: ')
    strength = check_password_strength(password)

    # Display password strength
    if strength == 5:
        print('Password strength: Very Strong')
    elif strength == 4:
        print('Password strength: Strong')
    elif strength == 3:
        print('Password strength: Medium')
    elif strength == 2:
        print('Password strength: Weak')
    else:
        print('Password strength: Very Weak')

    # Provide suggestions to improve password strength
    suggestions = provide_suggestions(strength, password)
    print("\nSuggestions to improve your password:")
    for suggestion in suggestions:
        print("- " + suggestion)


if __name__ == '__main__':
    main()
