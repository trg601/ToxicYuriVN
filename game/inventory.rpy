default inventory_items = []
default green_inventory_items = []
default folder_open = False

init python:
    config.overlay_screens.append("inventory")

    class InventoryItem:
        def __init__(self, name: str, description: str, image: str):
            self.name = name
            self.description = description
            self.image = image
            self.is_hovered = False
    
    def try_add_inventory_item(name: str, description: str, image: str, green_item: bool = False) -> bool:
        """Try to add an item to the inventory."""
        global folder_open
        item_list = green_inventory_items if green_item else inventory_items
        if not any(item.name == name for item in item_list):
            item_list.append(InventoryItem(name, description, image))    
            folder_open = True
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
    $ hover_item = None
    $ hover_index = 0

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
            # Red items
            $ inv_len = len(inventory_items)
            for i in range(max(3, len(inventory_items))):
                $ item = inventory_items[i] if i < inv_len else None
                vbox:
                    spacing 10
                    button:
                        xsize button_size
                        ysize button_size
                        add "gui/item slot red.png" xsize button_size ysize button_size
                        if item:
                            add item.image xsize button_size ysize button_size
                            action Notify("You clicked on " + item.name)
                            hovered SetField(item, "is_hovered", True)
                            unhovered SetField(item, "is_hovered", False)
                    if item and item.is_hovered:
                        $ hover_item = item
                        $ hover_index = i
            # Green items
            $ green_inv_len = len(green_inventory_items)
            for i in range(max(2, len(green_inventory_items))):
                $ item = green_inventory_items[i] if i < green_inv_len else None
                vbox:
                    spacing 10
                    button:
                        xsize button_size
                        ysize button_size
                        add "gui/item slot green.png" xsize button_size ysize button_size
                        if item:
                            add item.image xsize button_size ysize button_size
                            action Notify("You clicked on " + item.name)
                            hovered SetField(item, "is_hovered", True)
                            unhovered SetField(item, "is_hovered", False)
                    if item and item.is_hovered:
                        $ hover_item = item
                        $ hover_index = i + max(3, inv_len)
    
    if folder_open and hover_item:
        text hover_item.description color COLOR_HOVER style "outline_text":
            xpos (button_size + 30) * (hover_index + 1) + 20
            ypos button_size + 40

screen item_details(item):
    tag item_details

    text "AYO"

    vbox:
        xsize 300
        ysize 200

        text item.name
        text item.description