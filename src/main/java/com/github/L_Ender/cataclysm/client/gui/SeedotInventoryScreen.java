package com.github.L_Ender.cataclysm.client.gui;

import com.github.L_Ender.cataclysm.Cataclysm;
import com.github.L_Ender.cataclysm.entity.Pet.Seedot_Entity;
import com.github.L_Ender.cataclysm.inventory.SeedotMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class SeedotInventoryScreen extends AbstractContainerScreen<SeedotMenu> {
    private static final ResourceLocation SEEDOT_INVENTORY_LOCATION = new ResourceLocation(Cataclysm.MODID,"textures/gui/seedot_inventory.png");
    private final Seedot_Entity seedot;
    private float xMouse;
    private float yMouse;

    public SeedotInventoryScreen(SeedotMenu p_98817_, Inventory p_98818_, Seedot_Entity p_98819_) {
        super(p_98817_, p_98818_, p_98819_.getDisplayName());
        this.seedot = p_98819_;
    }

    protected void renderBg(GuiGraphics p_282553_, float p_282998_, int p_282929_, int p_283133_) {
        int i = (this.width - this.imageWidth) / 2;
        int j = (this.height - this.imageHeight) / 2;
        p_282553_.blit(SEEDOT_INVENTORY_LOCATION, i, j, 0, 0, this.imageWidth, this.imageHeight);

        p_282553_.blit(SEEDOT_INVENTORY_LOCATION, i + 70, j + 17, 0, this.imageHeight, seedot.getInventoryColumns() * 18, 54);
        InventoryScreen.renderEntityInInventoryFollowsMouse(p_282553_, i + 35, j + 62, 30, (float)(i + 35) - this.xMouse, (float)(j + 75 - 50) - this.yMouse, seedot);
    }

    public void render(GuiGraphics p_281697_, int p_282103_, int p_283529_, float p_283079_) {
        this.renderBackground(p_281697_);
        this.xMouse = (float)p_282103_;
        this.yMouse = (float)p_283529_;
        super.render(p_281697_, p_282103_, p_283529_, p_283079_);
        this.renderTooltip(p_281697_, p_282103_, p_283529_);
    }
}