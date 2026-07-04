from config.settings import Settings

def main():
    settings = Settings()
    print(f"Host: {settings.host}")
    print("Hello from redis-clone-in-python!")


if __name__ == "__main__":
    main()
