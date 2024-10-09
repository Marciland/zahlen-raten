[![codecov](https://codecov.io/github/Marciland/zahlen-raten/graph/badge.svg?token=NZXMH5J9GG)](https://codecov.io/github/Marciland/zahlen-raten)

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
