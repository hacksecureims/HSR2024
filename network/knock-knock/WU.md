# Knock knock

## Instructions 📝

Un administrateur de réseau s'est amusé à restreindre l'accès à un serveur smtp en bloquant le port.

Trouvez la combinaison gagnante pour accéder à son service. Le flag se trouve dans la bannière du serveur smtp.

Voici les informations de peering dont vous aurez besoin :

- Adresse du serveur : `10.22.148.20`

## Flag 🚩

`HSR{Who_is_there?}`

## Write-up 📝

Nous commençons par effectuer un scan des ports pour déterminer le port de départ.

```txt
$ nmap -Pn -p [-1024] -sT 10.22.148.20
[...]
PORT    STATE  SERVICE
25/tcp  closed smtp
957/tcp closed unknown
```

Nous utilisons ensuite netcat pour frapper les ports que nous trouvons, et lançons un scan pour trouver le port suivant.

```txt
$ for i in 957 521; do nc 10.22.148.20 $i; done; nmap -Pn -p [-1024] -sT 10.22.148.20
Ncat: Connection refused.
Ncat: Connection refused.
[...]
PORT    STATE  SERVICE
25/tcp  closed smtp
521/tcp closed ripng
720/tcp closed unknown
957/tcp closed unknown
```

A la fin, le port SMTP (tcp/25) nous est ouvert. Nous pouvons récupérer le flag.

```txt
$ for i in 957 521 720 123; do nc 10.22.148.20 $i; done
Ncat: Connection refused.
Ncat: Connection refused.
[...]
$ nc 10.22.148.20 25
220 ub22prod ESMTP Postfix HSR{Who_is_there?}
```
