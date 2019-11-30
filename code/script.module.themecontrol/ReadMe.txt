Requirements (In Your Addon):
    Settings.xml:
        - notifyvoice: This setting is for secondary sounds
        - theme: This setting should have matches to the folders in resources/skins/
            Example: resources/skins/main
                     resources/skins/alternate
    Resources Folder Structure:
        - skins
            - <theme_name>
                - xml: Contains your XMLs (Must be different name than normal skin addons use)
                - colors: Contains your colors.xml, formatted as directed in the docs and examples
                - media: Contains all your artwork
                - sounds: Contains the wav files for the sounds. Also has the sounds.xml as directed in docs and exampls
                
