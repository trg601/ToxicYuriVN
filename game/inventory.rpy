
default inventory_items = []
default folder_open = False

init python:
    config.overlay_screens.append("inventory")

    class InventoryItem:
        def __init__(self, name: str, description: str, image: str):
            self.name = name
            self.description = description
            self.image = image
            self.is_hovered = False
    
    def try_add_inventory_item(name: str, description: str, image: str) -> bool:
        """Try to add an item to the inventory."""
        global folder_open

        if not any(item.name == name for item in inventory_items):
            inventory_items.append(InventoryItem(name, description, image))                
            return True
        return False
    
    def clicked_inventory_icon():
        """Handle clicking on the inventory icon."""
        global folder_open

        folder_open = not folder_open
        if renpy.get_screen("minigame") and (game := renpy.get_screen_variable("game", screen="minigame")):
            game.click_inventory()

screen inventory:
    tag inventory

    zorder 1

    $ button_size = 100

    hbox:
        xoffset 30
        yoffset 30
        spacing 30

        button:
            xsize button_size
            ysize button_size
            action [Function(clicked_inventory_icon)]
            add ConditionSwitch(
                "folder_open", "gui/folder open.png",
                "not folder_open", "gui/folder closed.png"
            ) xsize button_size ysize button_size

        if folder_open:
            for item in inventory_items:
                vbox:
                    spacing 10
                    button:
                        xsize button_size
                        ysize button_size
                        add item.image xsize button_size ysize button_size
                        action Notify("You clicked on " + item.name)
                        hovered SetField(item, "is_hovered", True)
                        unhovered SetField(item, "is_hovered", False)
                    if item.is_hovered:
                        text item.description color COLOR_TEXT_MENU

screen item_details(item):
    tag item_details

    text "AYO"

    vbox:
        xsize 300
        ysize 200

        text item.name
        text item.description