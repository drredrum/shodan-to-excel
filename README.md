# Shodan Bulk Query

Skrypt ~~skradziony~~ zainspirowany przez:
https://github.com/emresaglam/shodan-bulk-ip-query

Jego przeznaczeniem jest ułatwienie wyszukiwania kontaktów do osób odpowiedzialnych za podatne urządzenia powiązane z adresami IP. Do zastosowania przy masowych wysyłkach pokroju Exchange, Citrix, Fortigate. Dla jego stosowania konieczne jest konto na Shodanie ze statusem "Membership" (można upolować za 5$ co jakiś czas), pozwala ono na używanie API. Klucz można znaleźć w https://account.shodan.io

**UWAGA** - limit zapytań dla planu "Memebership" wynosi 100 adresów IP miesięcznie, chociaż nie jest jasne, co liczy się do zużycia creditsów, jak na razie przetestowałem skrytp na kilkuset adresach i nie policzyło mi nic za to:
https://help.shodan.io/the-basics/credit-types-explained

Stan creditsów można monitorować tutaj:
https://developer.shodan.io/dashboard

# Wymagania
* `pip3 install -r requirements`
* Wklej swój klucz API do pliku `shodan_api_key.txt`.
* Przygotuj listę adresów IP w pliku `iplist.txt`, każdy adres w nowej linii. 

# Zastosowanie

`python3 shodanQuery.py` zaczyta listę IP z  `iplist.txt`, następnie zacznie pobierać informacje dla każdego adresu po kolei i wyświetlać informacje w terminalu:
```
[INFO] - fetching host 195.117.120.97, progress: 42.3%
```
W przypadku błędu pojawia się komunikat o przyczynie, np. brak IP w bazie Shodana, błąd połączenia, lub za szybkie requesty (w tym wypadku odpalamy skrypt jeszcze raz z `-d` i podajemy wartość pauzy w sekundach, domyślnie jest to 1 )

Skrypt bazowo wyrzuca dwa pliki do folderu output:
* `shodan_results_TIMESTAMP.json` - zawiera pełny zrzut informacji o adresach IP
* `shodan_results_TIMESTAMP.xlsx` - zawiera podstawowe informacje pomocne w ustaleniu adresów kontaktowych. Jeżeli Shodan nie ma wszystkich danych, to w odpowiednich komórkach pojawia się `-`. Jeżeli adres IP w ogóle nie występuje w bazie, do wszystkie komórki przyjmują wartości `NoData`. Dodatkowo dla xlsx są pobierane adresy abuse z WHOIS. Niestety narazie skrypt nie korzysta z RIPE, także ta funkcjonalność trochę ssie...

Dodatkowo jeżeli podczas pobierania informacji pojawią się IP, dla których wyskoczą błędy, ich lista zapisywana jest w:
`shodan_results_TIMESTAMP.txt`


