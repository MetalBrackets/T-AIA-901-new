
# Contribuer

## Git
```sh
# clone
git clone git@github.com:MetalBrackets/T-AIA-901.git

# New branch
git checkout -b feature/amazing-feature

# Pull Request
git push origin feature/amazing-feature # et ouvrir une PR sur Github

```

## Commits Conventionnels

L'utilisation des [Conventional Commit messages](https://www.conventionalcommits.org/en/v1.0.0/) permet la génération automatique du changelog, la création de PRs de release et la montée de version à partir de l'historique des commits. L'automatisation se fait grâce à une GitHub action  [release-please](https://github.com/googleapis/release-please) qui se déclanche lorsque des modification sont poussées sur la branche `main`

**- Format des commits**
```sh
# <type>[optional scope]: <description>
# ex :
feat(login): add captcha to login form
```

**- Usage pour auto-incrementer les versions**

| version | type de commit                        | description                                   |
| ------- | ------------------------------------- | --------------------------------------------- |
| major   | `feat!:`, `fix!:`, `refactor!:`, etc. | SemVer majeure : représente un changement majeur |
| minor   | `feat:`                               | SemVer mineure : Représente une nouvelle fonctionnalité |
| patch   | `fix:`,                               | SemVer patch : Représente des corrections de bugs |

🤖 Et voilà, c'est automatisé !