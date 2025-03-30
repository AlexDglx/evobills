# evobills
[WIP]

## Purpose
Testing selenium to autmate bill downloads on Evo car share evo.ca [evo.ca](https://evo-fo.vulog.center/login)

Download evo bills :
- Automated login (user must create a auth.json file)

_auth.json file_ :
```
{
    "authentification":
    {
        "username":"",
        "password":""
    }
}
```
### Current TODOs
- [x] Selenium auto login evo.ca
- [x] Navigate to billing. Download bills
- [ ] Download is skipping months
- [ ] Add pdf reader function
- [ ] Add parse pdf function
