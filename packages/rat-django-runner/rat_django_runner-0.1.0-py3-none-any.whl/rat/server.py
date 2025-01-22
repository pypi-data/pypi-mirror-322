import os
import subprocess


def runserver(ip="0.0.0.0", port=8000):
    """
    Django loyihasini ko'rsatilgan IP va portda ishga tushiradi.
    :param ip: Serverning IP-manzili (default: 0.0.0.0)
    :param port: Serverning porti (default: 8000)
    """
    try:
        # Django `manage.py` faylini qidiramiz
        if not os.path.exists("manage.py"):
            raise FileNotFoundError("manage.py fayli topilmadi. Django loyihasi katalogida ishga tushuring.")

        # `runserver` komandasi bilan serverni ishga tushirish
        command = f"python manage.py runserver {ip}:{port}"
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Xatolik: {e}")
