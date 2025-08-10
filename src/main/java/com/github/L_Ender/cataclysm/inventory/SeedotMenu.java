package com.github.L_Ender.cataclysm.inventory;

import com.github.L_Ender.cataclysm.entity.Pet.Seedot_Entity;
import net.minecraft.world.Container;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

public class SeedotMenu extends AbstractContainerMenu {
    private final Container seedotContainer;
    private final Seedot_Entity seedot;

    public SeedotMenu(int p_39656_, Inventory p_39657_, Container p_39658_, final Seedot_Entity p_39659_) {
        super((MenuType)null, p_39656_);
        this.seedotContainer = p_39658_;
        this.seedot = p_39659_;
        int i = 3;
        p_39658_.startOpen(p_39657_.player);
        int j = -18;

        for(int k = 0; k < 3; ++k) {
            for(int l = 0; l < ((Seedot_Entity)p_39659_).getInventoryColumns(); ++l) {
                this.addSlot(new SeedotSlot(p_39658_, 2 + l + k * ((Seedot_Entity)p_39659_).getInventoryColumns(), 71 + l * 18, 18 + k * 18));
            }
        }

        for(int i1 = 0; i1 < 3; ++i1) {
            for(int k1 = 0; k1 < 9; ++k1) {
                this.addSlot(new Slot(p_39657_, k1 + i1 * 9 + 9, 8 + k1 * 18, 102 + i1 * 18 + -18));
            }
        }

        for(int j1 = 0; j1 < 9; ++j1) {
            this.addSlot(new Slot(p_39657_, j1, 8 + j1 * 18, 142));
        }
    }

    public boolean stillValid(Player p_39661_) {
        return !this.seedot.hasInventoryChanged(this.seedotContainer) && this.seedotContainer.stillValid(p_39661_) && this.seedot.isAlive() && this.seedot.distanceTo(p_39661_) < 8.0F;
    }

    public ItemStack quickMoveStack(Player p_40199_, int p_40200_) {
        ItemStack itemstack = ItemStack.EMPTY;
        Slot slot = this.slots.get(p_40200_);
        if (slot != null && slot.hasItem()) {
            ItemStack itemstack1 = slot.getItem();
            itemstack = itemstack1.copy();
            if (p_40200_ < this.seedotContainer.getContainerSize()) {
                if (!this.moveItemStackTo(itemstack1, this.seedotContainer.getContainerSize(), this.slots.size(), true)) {
                    return ItemStack.EMPTY;
                }
            } else if (!this.moveItemStackTo(itemstack1, 0, this.seedotContainer.getContainerSize(), false)) {
                return ItemStack.EMPTY;
            }

            if (itemstack1.isEmpty()) {
                slot.setByPlayer(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
        }

        return itemstack;
    }

    public boolean mayPlace(ItemStack p_40231_) {
        return true;
    }

    public void removed(Player p_39663_) {
        super.removed(p_39663_);
        this.seedotContainer.stopOpen(p_39663_);
        if (seedot != null) seedot.setAttackState(5);
    }
}