# Is was DNS

## Instructions 📝

Une entreprise a exposé publiquement un serveur DNS par erreur.
Nous savons que l'entreprise possède le domaine `mycompany.com`.

C'est à vous de creuser et de voir si des informations intéressantes s'y cachent.

Voici les informations de peering dont vous aurez besoin :

- Adresse du serveur : `10.22.148.17`
- Port du serveur : `5353`

## Flag 🚩

`HSR{Just_a_simple_dns}`

## Write-up 📝

Soit par dictionnaire, soit par tâtonnement.
Nous avons trouvé un enregistrement TXT à l'adresse `flag.mycompany.com`.

```txt
$ dig @10.22.148.17 -p 5353 -t TXT flag.mycompany.com +short
JBJVE62KOVZXIX3BL5ZWS3LQNRSV6ZDOON6Q====
```

Un décodage du contenu en base32 plus tard, et le flag est trouvé.

```txt
$ printf "JBJVE62KOVZXIX3BL5ZWS3LQNRSV6ZDOON6Q====" | base32 -d
HSR{Just_a_simple_dns}
```
