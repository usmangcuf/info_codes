#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;

int main()
{
    ifstream file("//Users//mac//Downloads//info_codes//sample.txt"); // open file
    if (!file.is_open())
    {
        cout << "Error: Could not open file!" << endl;
        return 1;
    }

    // Arrays to hold counts
    int lower[26] = {0};
    int upper[26] = {0};
    int digits[10] = {0};
    int spaces = 0;

    char ch;
    while (file.get(ch))
    {
        if (ch >= 'a' && ch <= 'z')
        {
            lower[ch - 'a']++;
        }
        else if (ch >= 'A' && ch <= 'Z')
        {
            upper[ch - 'A']++;
        }
        else if (ch >= '0' && ch <= '9')
        {
            digits[ch - '0']++;
        }
        else if (ch == ' ')
        {
            spaces++;
        }
    }

    file.close();

    // Display results
    cout << "===== Alphabet and Digit Count =====" << endl;

    cout << "\nLowercase Letters:" << endl;
    for (int i = 0; i < 26; i++)
    {
        cout << char('a' + i) << " : " << lower[i] << endl;
    }

    cout << "\nUppercase Letters:" << endl;
    for (int i = 0; i < 26; i++)
    {
        cout << char('A' + i) << " : " << upper[i] << endl;
    }

    cout << "\nDigits:" << endl;
    for (int i = 0; i < 10; i++)
    {
        cout << i << " : " << digits[i] << endl;
    }

    cout << "\nSpaces: " << spaces << endl;

    return 0;
}
