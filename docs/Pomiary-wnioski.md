#### Wnioski z pomiarów CRUD'u i raportów

Porównując czasy wykonywania operacji bezpośrednio na bazie danych możemy zaobserwować, że różnice między nimi są dość 
niewielkie (przy pomiarze dla stu operacji). Zarówno zapytania dla raportów jak i dotyczące produktów odbiegają od 
siebie o milisekundy.

Natomiast odnosząc się do pomiarów uzyskanych przez api widzimy już spore rozbieżności w wynikach. Dla prostych operacji 
`select` na tabeli `products` wynik to w przybliżeniu 7 sekund przy czym generowanie stu raportów odnośnie uzupełnienia 
stanu magazynowego dla produktów zajeło już około 43 sekundy. Było to również zapytanie `select` z tym, że łączenie 
danych z poszczególnych kolumn zapewniło dodatkowy narzut czasowy.

W zestawieniu poszczególnych czasów operacji wykonywanych bezpośrednio na bazie danych z pomiarami na api widzimy, że 
wzrastają one znacznie wraz z poziomem komplikacji zapytania. Dla prostego `select` różnica jest niemal dwukrotna. Przy 
`update` czterokrotna. Natomiast pomiar dla raportu `reorder` wykazał aż dziewięciokrotność czasu wykonania tej samej 
operacji bezpośrednio na bazie danych.

Co do interpretacji wyników oczywiście należy przyjąć pewną poprawkę ze względu na to, że API komunikowało się z bazą 
poprzez jej kontener. Natomiast skrypty `.sh` były uruchamiane w jego wnętrzu co mogło również wpłynąć na pomiary. 
Trzeba też przyjąć, że pewien czas został poświęcony na walidację modeli i kod zależny od danego endpointu. Nie mniej 
jednak różnice w przypadku bardziej skomplikowanych operacji są spore i przy projektowaniu tego typu aplikacji należy 
mieć to na uwadzę.
