import os


def generate_folders():
    if not os.path.exists('accaunts_data/'):
        os.mkdir('accaunts_data')
    
    if not os.path.exists('last_followers/'):        
        os.mkdir('last_followers')
    
    if not os.path.exists('screenshots/'):
        os.mkdir('screenshots')
    
    if not os.path.exists('photoshop_files/'):
        os.mkdir('photoshop_files')
    
    if not os.path.exists('pics_to_send/'):
        os.mkdir('pics_to_send')
    
        
if __name__ == "__main__":
    generate_folders()
    