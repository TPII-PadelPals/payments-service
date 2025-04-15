# FastAPI Service Template

## Requirements

- [Docker](https://www.docker.com/) to containerize the app.
- [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Workflow

#### Dependencies are managed with **uv**.

Install it by running:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once installed, you can run to sync & install dependencies:

```bash
uv sync
```

You can activate the virtual environment with:

```bash
source .venv/bin/activate
```

Finally, activate **pre-commit**:

```bash
pre-commit install
```

### Without docker

Run API with:

```bash
fastapi dev --reload app/main.py
```

### With docker

Start the local stack with Docker Compose (API + Postgres):

```bash
docker compose watch
```

#### Now you can interact with the API:

- JSON based web API based on OpenAPI: http://localhost:8000

- Automatic interactive documentation with Swagger UI: http://localhost:8000/docs

- Postgres db: http://localhost:5440

#### To check the logs, run (in another terminal):

```bash
docker compose logs
```

## Environment variables

The `.env` file contains all the configuration data.

Each environment variable is set up in the `.env` file for dev, but to let it prepared for our CI/CD system, the `docker-compose.yml` file is set up to read each specific env var instead of reading the `.env` file.

## Pre-commits, code linting & code formatting

We are using a tool called [pre-commit](https://pre-commit.com/) for code linting and formatting.

It runs right before making a commit in git. This way it ensures that the code is consistent and formatted even before it is committed.

You can find a file `.pre-commit-config.yaml` with configurations at the root of the project.

**To lint manually:**

```bash
bash scripts/lint.sh
```

**To format code manually:**

```bash
bash scripts/format.sh
```

## Test Coverage

When the tests are run, a file **htmlcov/index.html** is generated, you can open it in your browser to see the coverage of the tests.

To run test manually:

```bash
bash scripts/test.sh
```

## VS Code compatibility

There are already configurations in place to run the backend through the VS Code debugger, so that you can use breakpoints, pause and explore variables, etc. File with config located at `.vscode/launch.json`. If this repo is in within a workspace, move this config to the workspace root.

The setup is also already configured at `.vscode/settings.json` so you can run the tests through the VS Code Python tests tab.

## Links

- https://fastapi.tiangolo.com/tutorial/bigger-applications/
- https://docs.astral.sh/uv/
- https://pre-commit.com/

## Mercado Pago

### Setup Ngrok
MercadoPago does not offer a fully local development framework, so it will be needed to deploy the payment-service in order for it to fully interact with MercadoPago.

Here, we propose to use Ngrok which is a reverse proxy that allows to create secure tunnels between local apps and free public random domains. Follow installation steps in [ngrok-setup](https://dashboard.ngrok.com/get-started/setup).

After installation, run ngrok as follows to deploy payment-service running on port 8004:
```
ngrok http http://localhost:8004
```
The previous command will result in an output similar the next one:
```
Session Status                online                                                                                    Account                       your-account@gmail.com (Plan: Free)                                                     Update                        update available (version 3.22.1, Ctrl-U to update)                                       Version                       3.20.0                                                                                    Region                        South America (sa)                                                                        Latency                       43ms                                                                                      Web Interface                 http://127.0.0.1:4040                                                                     Forwarding                    https://b744-181-171-9-247.ngrok-free.app -> http://localhost:8004                                                                                                                                                Connections                   ttl     opn     rt1     rt5     p50     p90                                                                             13      0       0.00    0.00    5.83    6.52
```

If your remark the `Forwarding` section, you will see URL in which the local app was deployed by tunneling it to localhost. Save this URL as it will be need in the following sections.

### Setup MercadoPago
#### 1. Create MercadoPago account
Create MercadoPago account or use existing one. Although, it will only be used for creating test accounts, it is recommended to create a new account to avoid using your personal wallet information in the project configuration.

#### 2. Create tests accounts
Follow steps in [integration-test](https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/integration-test) to create two MercadoPago test accounts: one for the **seller** and one for the **buyer**. After creating them, copy their usernames and passwords somewhere you can access them quickly as they will be needed very often.

#### 3. Create test app
Log into the **seller** test account and create a MercadoPago app as described in [create-application](https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/create-application).

#### 4. Recover production 'Access Token'
After creation, follow the steps in [go-to-production](https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/go-to-production) to find the `Access Token`. Copy its value and assign it to the `MERCADO_PAGO_PROD_ACCESS_TOKEN` variable in you `.env` file. This one will be used to generate payment in the project.

#### 5. Setup notifications
MercadoPago use webhooks to notify our app of all the events that occur during payment exection. Follow steps in [webhooks](https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/webhooks) to setup webhooks in _Modo productivo_, using the following values:
- _URL de produccion_: Concatenate **Ngrok forwarding URL** with `/api/v1/payments/notifications/mercadopago`
- _Eventos_: Click on _Pagos_ and _Ordenes comerciales_
Once saved the configuration, a `Secret key` (_Clave secreta_) will be enable. Copy its value and assign it to the `MERCADO_PAGO_NOTIFICATION_SECRET_KEY` variable in your `.env` file.
**Important!**: Every time you start a new ngrok forwarding, it will be needed to update the webhook notifications url. However, the secret key will remain the same, as long as, you don't restart it.
In order to test the webhook, click on the button _Simular notificacion_ and set the following values:
- URL: Set the _URL de produccion_.
- _Tipo de evento_: Set _Pago_
- Data ID: Set a numerical value and copy it to the `MERCADO_PAGO_NOTIFICATION_TEST_ID` variable in the `.env` file.

### Test
#### 1. Create payment order
Open FastAPI `/doc` page on localhost (http://localhost:8004) or ngrok URL and execute the following request:
```
POST /api/v1/payments
{
  "match_public_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "match_title": "PadelPals Match: PadelFIUBA 15-04-2025 10 hs",
  "user_telegram_id": <your-bot-chat-id>,
  "amount": 1000
}
```
Resulting in a similar response to the next one:
```
{
  "match_public_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "match_title": "PadelPals Match: PadelFIUBA 15-04-2025 10 hs",
  "user_telegram_id": <your-bot-chat-id>,
  "amount": 1000,
  "url": "https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id=2388152558-e3c73e93-3caf-4ce1-ada6-a2a414a6e74f"
}
```
Save the `url` value for the following section.

#### 2. Pay with MercadoPago
Log out from every MercadoPago account of every browser. Then copy the payment `url` obtained from the response to the previous request and paste into the browser. This will redirect you to MercadoPago app in order to pay the generated payment order. Log in using the **buyer** account and proceed to pay the transaction using one of the following methods:
- Pay with MercadoPago money (obtained with the creation of the account)
- Pay using a debit / credit card (only available when the transaction amount surpass certain threshould). See [test-cards](https://www.mercadopago.com.ar/developers/es/docs/checkout-api/integration-test/test-cards).

Note: If the MercadoPago requires a verification code to complete the transaction, use the last 6 numbers of the **buyer** Access Token (only available after creating a MercadoPago app with this account).

#### 3. See MercadoPago notifications
As we setup up earlier, MercadoPago will send notifications to `/api/v1/payments/notifications/mercadopago` are handled and displayed in `docker compose logs`. Notifications of type `merchant_orders` and `payments`, will log `[Merchant Order] '<match_title>': <DONE/WIP>`, whereas every other will display the request query params, headers and body.
