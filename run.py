import os
import sys

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    app_path = os.path.join(base_path, "app.py")
    
    sys.argv = ["streamlit", "run", app_path, "--server.headless=true", "--global.developmentMode=false"]
    from streamlit.web.cli import main
    main()