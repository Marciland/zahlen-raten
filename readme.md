[![Frontend codecov](https://codecov.io/github/Marciland/zahlen-raten/graph/badge.svg?token=NZXMH5J9GG&flag=frontend)](https://codecov.io/github/Marciland/zahlen-raten)
[![Backend codecov](https://codecov.io/github/Marciland/zahlen-raten/graph/badge.svg?token=NZXMH5J9GG&flag=backend)](https://codecov.io/github/Marciland/zahlen-raten)
![Coverage Sunburst](https://codecov.io/github/Marciland/zahlen-raten/graphs/sunburst.svg?token=NZXMH5J9GG)

cd frontend
npm install
npm run unit-test
npm run dev
npm run e2e-test
(npm run e2e-debug)

cd backend
pip install -r requirements.txt
python -m pytest --cov=modules --cov=database
python main.py
