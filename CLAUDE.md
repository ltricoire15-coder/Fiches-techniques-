# Fiches techniques bac pro TCVA

`index.html` est le site des fiches. Le lien Google Apps Script de l'enseignant(e) lit ce fichier
directement sur GitHub (branche `main`) : chaque push met le lien à jour.

## Règles à respecter pour toute fiche (nouvelle ou modifiée)

- Une fiche = un objet dans le tableau `S` de `index.html`. Ne jamais changer la mise en page
  d'une seule fiche : l'affichage est commun à toutes (tableau `FIELDS`).
- Les 16 rubriques, toujours dans cet ordre, toutes remplies :
  nom commun (`n`), genre et espèce (`sci`), statut juridique (`st` : `D` ou `N`, note `stn` facultative),
  embranchement et classe (`emb`, `cla`, déduits du groupe sauf invertébrés), ordre (`ord`),
  famille (`fam`, format « Cyprinidés (Cyprinidae) »), origine (`ori`), biotope (`bio`),
  régime alimentaire (`reg`), reproduction (`rep`), dimorphisme sexuel (`dim`), comportement (`comp`),
  accessoires (`acc`), paramètres (`par` ; libellé `pl` : eau pour les poissons, température et humidité
  pour amphibiens/reptiles, température pour les autres), durée de vie (`vie`), taille adulte (`tai`).
- Groupe `g` : `poi`, `amp`, `rep`, `ois`, `mam` ou `inv`. Les espèces d'un même ordre et d'une même
  famille restent regroupées dans le tableau.
- Badge : `ok:true` uniquement pour les fiches envoyées par l'enseignant(e) (« ✓ Vérifié »).
  Toute fiche rédigée par Claude reste sans `ok` (« ⚠ À vérifier »).
- Formats : températures « 22 – 28 °C », pH « pH 6 – 7,5 », dureté « GH 5 – 15 °dGH ».
