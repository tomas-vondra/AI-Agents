# Run

```bash
docker volume create mssql_data

docker run --name mssql -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Heslo_1234" -v mssql_data:/sql_data -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
```
