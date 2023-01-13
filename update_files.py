import dload

if __name__ == '__main__':
    url = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/30e783e4-2bec-4a7d' \
          '-bb22-ee3e3b26ca96/download/gtfsgoogle.zip '
    dload.save_unzip(url, delete_after=True)
