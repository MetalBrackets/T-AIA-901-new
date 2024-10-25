# Versionner les gros fichiers

Le fichier `model/model/save/tf_model.h5` fait 676Mo et dépasse la taille limite de fichier GitHub de 100Mo.

```sh
# erreur remonté
remote: error: GH001: Large files detected.
You may want to try Git Large File Storage - https://git-lfs.github.com
```

## Git LFS

**Installation sur votre OS**  
-> https://git-lfs.com/

**Les actions qui ont été faites sur le repository**    
- Initialisation de Git LFS -> `git lfs install`
- config des fichiers à tracker dans le .gitattributes  
    -> avec un filtre sur les .h5
