def shell():
    while True:
        try:
            command = input("$ ").strip().split()
            if not command:
                continue
                
            cmd = command[0]
            args = command[1:]
            '''
            if cmd == "cd":
                cd(args)
            elif cmd == "ls":
                ls(args)
                '''
            # ... другие команды
                
        except KeyboardInterrupt:
            print("\nExiting shell...")
            break
        except Exception as e:
            print(f"Error: {e}")