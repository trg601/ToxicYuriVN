default inventory_items = [None] * 5
default folder_open = False

init python:
    config.overlay_screens.append("inventory")

    class InventoryItem:
        def __init__(self, name: str, description: str, image: str):
            self.name = name
            self.description = description
            self.image = image
            self.is_hovered = False
    
    def try_add_inventory_item(name: str, description: str, image: str, index: int = None) -> bool:
        """Try to add an item to the inventory."""
        global folder_open
        if True == True or not any(item.name == name for item in inventory_items):
            if index is not None and 0 <= index < len(inventory_items) and inventory_items[index] is None:
                inventory_items[index] = InventoryItem(name, description, image)
            else:
                inventory_items.insert(len(inventory_items), InventoryItem(name, description, image))
            folder_open = True
            return True
        return False

    def close_inventory():
        """Close the inventory screen."""
        global folder_open
        folder_open = False
    
    def clicked_inventory_icon():
        """Handle clicking on the inventory icon."""
        global folder_open

        folder_open = not folder_open
        if renpy.get_screen("minigame") and (game := renpy.get_screen_variable("game", screen="minigame")):
            game.click_inventory()
    
    def has_all_dangerous_items() -> bool:
        """Check if the player has all dangerous items."""
        dangerous_items = ["Relic", "Garlic", "Rice"]
        return all(item in (item.name for item in inventory_items if item) for item in dangerous_items)

    def has_all_upgrade_items() -> bool:
        """Check if the player has all upgrade items."""
        upgrade_items = ["Weedwhacker", "Bucket"]
        return all(item in (item.name for item in inventory_items if item) for item in upgrade_items)

screen inventory_item(item, button_size, image):
    vbox:
        spacing 10
        button:
            xsize button_size
            ysize button_size
            add f"gui/item slot {image}.png" xsize button_size ysize button_size
            if item:
                add item.image xsize button_size ysize button_size
                action Notify("You clicked on " + item.name)
                hovered SetField(item, "is_hovered", True)
                unhovered SetField(item, "is_hovered", False)

screen inventory:
    tag inventory

    zorder 1

    $ button_size = 100
    $ hover_item = None
    $ hover_index = 0

    hbox:
        xoffset 15
        yoffset 15
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
            $ inv_len = len(inventory_items)
            for i in range(max(5, inv_len)):
                $ red = (i % 2 == 0)
                $ item = inventory_items[i] if i < inv_len else None
                use inventory_item(item, button_size, "red" if red else "green")
                if item and item.is_hovered:
                    $ hover_item = item
                    $ hover_index = i
    
    # Show item details if hovered
    if folder_open and hover_item:
        text hover_item.description color COLOR_HOVER style "outline_text":
            xpos (button_size + 30) * (hover_index + 1) + 20
            ypos button_size + 40
