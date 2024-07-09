import webhook
import asyncio



if __name__ == '__main__':
    emb = webhook.make_embed_season3()
    asyncio.run(webhook.send_webhook(emb))